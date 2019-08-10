""""
    DeskUnity
    Interface Class
"""
import re
import socket
import logging
import subprocess
import multiprocessing
import multiprocessing.dummy

from core.os import OS
from core.event import Event
from subprocess import Popen
from core.encoders.event_encoder import EventEncoder
from Configs import ENCODE_FORMAT, PORT, SERVER_CONNECT_TIMEOUT


class Interface:

    __interfaces = []
    __active_hosts = []
    __active_server = []
    __lan = "ethernet"

    @staticmethod
    def __get_interfaces_windows(skip_no_gateway=True):
        """ Returns Windows Interfaces """
        output = subprocess.check_output("ipconfig /all")

        lines = output.splitlines()
        lines = filter(lambda x: x, lines)

        ip_address = ''
        mac_address = ''
        name = ''
        gateway = ''
        description = ''
        lan = False

        for line in lines:
            # -------------
            # Interface Name
            line = line.decode(ENCODE_FORMAT)
            is_interface_name = re.match(r'^[a-zA-Z0-9].*:$', line)
            if is_interface_name:

                # Check if there's previews values, if so - yield them
                if name and ip_address and mac_address and gateway and description:
                    if skip_no_gateway:
                        if len(gateway) < 1:
                            pass
                        else:
                            yield {
                                "ip_address": ip_address,
                                "mac_address": mac_address,
                                "name": name,
                                "gateway": gateway,
                                "description": description,
                                "lan": lan
                            }

                ip_address = ''
                mac_address = ''
                name = line.rstrip(':')
                gateway = ''
                description = ''
                lan = False

            line = line.strip().lower()

            if ':' not in line:
                continue

            value = line.split(':')[-1]
            value = value.strip()

            is_gateway = re.match(r'default gateway', line)

            if is_gateway:
                gateway = value
                gateway = gateway.strip()

            is_description = not description and re.match(r'description', line)

            if is_description:
                description = value
                description = description.strip()

                if Interface.__lan in description.lower():
                    lan = True

            # -------------
            # IP Address

            is_ip_address = not ip_address and re.match(r'ipv4 address|autoconfiguration ipv4 address|ip address', line)

            if is_ip_address:
                ip_address = value
                ip_address = ip_address.replace('(preferred)', '')
                ip_address = ip_address.strip()

            # -------------
            # MAC Address

            is_mac_address = not ip_address and re.match(r'physical address', line)

            if is_mac_address:
                mac_address = value
                mac_address = mac_address.replace('-', ':')
                mac_address = mac_address.strip()

        if name and ip_address and mac_address and gateway:
            if skip_no_gateway:
                if len(gateway) < 1:
                    pass
                else:
                    yield {
                        "ip_address": ip_address,
                        "mac_address": mac_address,
                        "name": name,
                        "gateway": gateway,
                        "description": description,
                        "lan": lan
                    }

    @staticmethod
    def get_interfaces():
        """ Returns Interfaces """
        return Interface.__get_interfaces_windows()

    @staticmethod
    def get_all_ips_for_gateway(gateway):
        split_gateway = gateway.split(".")
        for i in range(1, 255):
            split_gateway[-1] = str(i)
            yield ".".join(split_gateway)

    @staticmethod
    def __is_host_alive(host):
        try:
            cmd = ["ping", "-c", "1", "-w", "1000", host]  # Todo: Default Linux Command, cant create issues :D
            if OS.get() == OS.WINDOWS:
                cmd = ["ping", "-n", "1", "-w", "1000", host]
            elif OS.get() == OS.LINUX:
                cmd = ["ping", "-c", "1", "-w", "1000", host]
            pipe = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = pipe.communicate()
            if error:
                pass
            if b'Lost = 0' in output:
                Interface.__active_hosts.append(host)
        except subprocess.CalledProcessError:
            pass
        except Exception as e:
            logging.error("Exception in ping subprocess")
            logging.exception(e)

    @staticmethod
    def get_all_alive_ips():
        Interface.__interfaces = list(Interface.get_interfaces())
        for interface in Interface.get_interfaces():
            gateway = interface['gateway']
            num_threads = 50 * multiprocessing.cpu_count()  # Number of thread
            pool = multiprocessing.dummy.Pool(num_threads)
            pool.map(Interface.__is_host_alive, Interface.get_all_ips_for_gateway(gateway))
        return Interface.__active_hosts

    @staticmethod
    def get_gateway_for_ip(ip):
        ip_parts = ip.split(".")
        ip_parts[-1] = "1"
        return ".".join(ip_parts)

    @staticmethod
    def get_interface_by_ip(ip):
        """ Returns Interface object of the ip"""
        try:
            for interface in Interface.__interfaces:
                if interface["gateway"] == Interface.get_gateway_for_ip(ip):
                    return interface
        except Exception as e:
            logging.error("Exception in get_interface_by_ip")
            logging.exception(e)
            return None

    @staticmethod
    def __is_server(host):
        """" Returns true if given host is a server """
        try:
            socket.setdefaulttimeout(SERVER_CONNECT_TIMEOUT)
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.connect((host, PORT))
            Interface.__active_server.append(host)
            event = Event(Event.CONNECTION_TEST)
            socket_.send(EventEncoder.encode(event))
            socket_.close()
            logging.debug("Test connection to {}:{} closed.".format(host, PORT))
        except socket.timeout:
            pass
        except ConnectionRefusedError:
            pass
        finally:
            socket.setdefaulttimeout(None)

    @staticmethod
    def get_desk_unity_servers():
        """" Return list of desk unity servers """
        if len(Interface.__active_hosts) == 0:
            Interface.get_all_alive_ips()
        num_threads = 50 * multiprocessing.cpu_count()  # Number of thread
        pool = multiprocessing.dummy.Pool(num_threads)
        pool.map(Interface.__is_server, Interface.__active_hosts)
        return Interface.__active_server

