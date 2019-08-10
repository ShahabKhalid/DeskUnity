""""
    DeskUnity 1.0
    Server Class
"""
import socket
import logging
import threading

from core.event import Event
from core.handlers.event_handler import EventHandler
from core.encoders.event_encoder import EventEncoder
from Configs import ENCODE_FORMAT, PENDING_QUEUE_COUNT, HOST, PORT, ALLOWED_CLIENTS, EVENT_SEPARATOR


class Server:

    class Client:
        connection = None
        address = None

        def __init__(self, connection, address):
            self.connection = connection
            self.address = address

    def __init__(self):
        """" Server instance constructor"""
        try:
            self.clients = {}
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.info("Binding to {}:{}".format(HOST, PORT))
            self.socket.bind((HOST, PORT))
            pass
        except Exception as e:
            logging.error("Unable to init server instance.")
            logging.exception(e)

    def start_listening(self, computer):
        """" Start listening """
        while computer.is_running:
            try:
                self.socket.listen(PENDING_QUEUE_COUNT)
                logging.info("Server is now listening for client computers...")
                connection, address = self.socket.accept()
                self.on_client_connect(connection, address, computer)
            except Exception as e:
                if not computer.is_running:
                    exit()
                logging.error("Unable to start server listening, retrying....")
                logging.exception(e)

    def start_listening_thread(self, computer):
        """" Start listening on thread """
        try:
            threading.Thread(target=self.start_listening, args=(computer,)).start()
        except Exception as e:
            logging.error("Unable to start server listening thread.")
            logging.exception(e)

    def on_client_connect(self, connection, address, computer):
        """" Callback on client connection """
        try:
            logging.debug(f"Client {address} connected.")
            if len(self.clients) < ALLOWED_CLIENTS:
                self.clients[address] = self.Client(connection, address)
                self.event_receiver_thread(self.clients[address], computer)
            else:
                logging.debug(f"Client {address} is kicked, clients limit reached.")
                self.kick(self.clients[address])
        except Exception as e:
            logging.error("Exception occurred on client connect callback.")
            logging.exception(e)

    def on_client_disconnect(self, client):
        """" Callback on client disconnection """
        try:
            self.clients[client.address] = None
            client.connection = None
            if client.address in self.clients:
                del self.clients[client.address]
            logging.debug(f"Client {client.address} disconnected.")
        except Exception as e:
            logging.error("Exception occurred on client disconnect callback.")
            logging.exception(e)

    def event_receiver(self, client, computer):
        """" Events receiver """
        try:
            if client.address in self.clients:
                while client.connection and computer.is_running:
                    events = client.connection.recv(1024)
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
                            event.client = client
                            EventHandler.handle(event)

                            if event.name == Event.CONNECTION_TEST:
                                self.kick(client)
                                break   # Stop receiving
            else:
                logging.warning("Client {} is disconnected or kicked.".format(client.address))
                logging.info("Closing event receive thread for {}".format(client.address))
        except ConnectionResetError:
            self.on_client_disconnect(client)
            logging.warning("Client {} is disconnected".format(client.address))
            logging.info("Closing event receive thread for {}".format(client.address))
        except Exception as e:
            logging.error("Exception occurred on server event receive.")
            logging.exception(e)

    def event_receiver_thread(self, client, computer):
        """" Event receiving on thread """
        try:
            threading.Thread(target=self.event_receiver(client, computer,)).start()
        except Exception as e:
            logging.error("Exception occurred on server event receive thread.")
            logging.exception(e)

    def send_event(self, client, event):
        """" Send event to client """
        try:
            if client.address in self.clients:
                client.connection.sendall(EventEncoder.encode(event))
            else:
                logging.warning("Client {} is disconnected or kicked.".format(client.address))
        except Exception as e:
            logging.error("Exception occurred on server send event.")
            logging.exception(e)

    def kick(self, client):
        try:
            # Disconnect Client
            client.connection.close()
            self.on_client_disconnect(client)
        except Exception as e:
            logging.error("Exception occurred on client kick.")
            logging.exception(e)

    def shutdown(self):
        try:
            event = Event(Event.SERVER_SHUT)
            for address in self.clients:
                self.clients[address].connection.sendall(EventEncoder.encode(event))
            self.socket.close()
        except Exception as e:
            logging.error("Exception occurred on server shutdown.")
            logging.exception(e)
