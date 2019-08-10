""""
    DeskUnity 1.0
    Client Class
"""
import socket
import logging
import threading

from core.event import Event
from Configs import ENCODE_FORMAT, EVENT_SEPARATOR
from core.encoders.event_encoder import EventEncoder
from core.handlers.event_handler import EventHandler


class Client:

    class Server:
        socket_ = None
        connected = False

        def __init__(self, socket_):
            self.socket_ = socket_

    def __init__(self):
        """" Client instance Constructor """
        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server = self.Server(socket_)
        except Exception as e:
            logging.error("Unable to init client instance.")
            logging.exception(e)

    def connect(self, host, port, computer):
        """" Connects on a server"""
        try:
            logging.info("Connecting to the server {}:{}".format(host, port))
            self.server.socket_.connect((host, port))
            self.server.connected = True
            event = Event(Event.TEST)
            self.server.socket_.send(EventEncoder.encode(event))
            logging.info("Connected to the server.")
            self.event_receiver_thread(computer)
        except Exception as e:
            logging.error("Unable to connect to server.")
            logging.exception(e)

    def event_receiver(self, computer):
        """" Events / Messages Receiver """
        try:
            logging.debug("Starting event receiving thread...")
            while self.server.connected:
                events = self.server.socket_.recv(1024)
                print(events)
                if len(events) < 1:
                    continue
                events = events.decode(ENCODE_FORMAT).split(EVENT_SEPARATOR)
                logging.debug(events)
                for event in events:
                    if len(event) <= 1:
                        continue
                    logging.debug(event)
                    event = EventEncoder.decode(event)
                    if event is not None:                        
                        event.computer = computer
                        event.client = self
                        EventHandler.handle(event)
        except (ConnectionResetError, ConnectionAbortedError):
            self.disconnect()
        except Exception as e:
            logging.error("Exception on client event receiver.")
            logging.exception(e)

    def event_receiver_thread(self, computer):
        """" Events / Messages Receiver on thread """
        try:
            threading.Thread(target=self.event_receiver, args=(computer,)).start()
        except Exception as e:
            logging.error("Exception on client event receiver thread.")
            logging.exception(e)

    def send_event(self, event):
        """" Send event to server """
        try:
            if not isinstance(event, Event):
                raise Exception("Invalid event passed.")
            if self.server is not None and self.server.socket_ is not None:
                self.server.socket_.sendall(EventEncoder.encode(event))
                logging.debug("Event {} sent to server".format(event.name))
            else:
                logging.warning("You are disconnected from server.")
        except Exception as e:
            logging.error("Exception occurred on client send event.")
            logging.exception(e)

    def disconnect(self):
        """" Disconnects from server """
        try:
            if self.server:
                self.server.connected = False
                self.server.socket_.close()
            self.server = None
        except Exception as e:
            logging.error("Exception occurred on client disconnect.")
            logging.exception(e)
