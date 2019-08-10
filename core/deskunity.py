""""
    DeskUnity 1.0
    Starter Class
"""
import logging
import threading

from gui import GUI
from core.interface import Interface
from core.computer import Computer

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s'
)


class DeskUnity:

    this_computer = None
    app = None
    thread = None

    def __init__(self):
        self.app = GUI(exit_handler=self.exit_handler)

    def show_ui(self):
        self.app.show()

    def start(self):
        logging.info("Starting DeskUnity...")
        # app = GUI()

        def run():
            self.app.ui.set_status("Searching for servers...")
            servers = Interface.get_desk_unity_servers()
            self.this_computer = Computer()
            if len(servers) == 0:
                self.app.ui.set_status("No server founds.")
                logging.info("No server found.")
                self.app.ui.set_status("Starting as server.")
                self.this_computer.start_server()
                self.app.ui.set_status("Server Started.")
                return True
            else:
                lan_server = servers[0]
                if len(servers) > 1:
                    self.app.ui.set_status("Found more than one server, choosing best interface...")
                    for server in servers:
                        interface = Interface.get_interface_by_ip(server)
                        if interface["lan"]:
                            lan_server = server
                    self.app.ui.set_status("Connecting to server...")
                    self.this_computer.connect_to_server(lan_server)
                else:
                    server = servers[0]
                    self.app.ui.set_status("Connecting to server...")
                    self.this_computer.connect_to_server(server)
                self.app.ui.set_status("Connected to server.")
                return False
        self.thread = threading.Thread(target=run)
        self.thread.start()

    def exit_handler(self):
        if self.this_computer.is_server():
            self.this_computer.stop_server()
        else:
            self.this_computer.stop_client()
