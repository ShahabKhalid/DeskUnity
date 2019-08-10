"""
    DeskUnity 1.0
    Computer Class
"""
import logging

from screeninfo import get_monitors
from pynput.mouse import Controller

from core.os import OS
from comm.server import Server
from comm.client import Client
from Configs import PORT
from events.hook import Hook
from core.encoders.event_encoder import Event


class Computer:

    __is_server = None
    __server = None
    __client = None
    __hook = None
    __position = 0  # positive values is right and negative is left
    __active_computer_position = 0

    is_running = False

    __mouse = Controller()
    __old_x = None
    __old_y = None

    class MousePos:
        x = None
        y = None

        def __init__(self, x, y):
            self.x = x
            self.y = y

    def __init__(self):
        """ Computer Constructor """
        self.__is_server = False
        self.__monitors = get_monitors()
        # Todo: Too be change in next version
        if len(self.__monitors) > 1:
            logging.error("Current version of DeskUnity only supports one monitor per computer.")
            exit()
        self.__width = self.__monitors[0].width
        self.__height = self.__monitors[0].height
        # -----------------------------------

    def start_server(self):
        """ Start server in computer """
        self.__server = Server()
        self.is_running = True
        self.__server.start_listening_thread(self)
        self.__is_server = True
        self.__position = 0     # Centered Computer
        self.__hook = Hook(self.mouse_handler, self.keyboard_handler)
        self.__hook.hook_mouse()
        self.__hook.hook_keyboard()

    def stop_server(self):
        self.is_running = False
        self.stop_hooks()
        self.__server.shutdown()
        del self.__server

    def stop_client(self):
        self.is_running = False
        self.__client.disconnect()

    def stop_hooks(self):
        self.__hook.unhook_keyboard()
        self.__hook.unhook_mouse()

    def get_server(self):
        """ Returns server instance """
        return self.__server

    def is_server(self):
        """ Returns is computer a server """
        return self.__is_server

    def get_client(self):
        """ Returns client instance """
        return self.__client

    def get_hook(self):
        """ Returns client hook instance """
        return self.__hook

    def get_position(self):
        return self.__position

    def connect_to_server(self, server):
        """ Connects to the server """
        self.__client = Client()
        self.__client.connect(server, PORT, self)
        self.__position = 1     # Right Computer / Position

    def get_mouse_movement(self, x, y):
        if self.__old_x is None and self.__old_y is None:
            self.__old_x, self.__old_y = self.__mouse.position

        move_x, move_y = x - self.__old_x, y - self.__old_y
        self.__old_x, self.__old_y = self.__mouse.position
        return self.MousePos(move_x, move_y)

    def set_active_computer_position(self, position):
        self.__active_computer_position = position

    def get_active_computer_position(self):
        return self.__active_computer_position

    def get_active_computer_client(self):
        clients = self.get_server().clients
        # Todo: For now I am sending 0 indexed client as only one client in ALLOWED for now
        for key in clients:
            return clients[key]

    def mouse_handler(self, event):
        """ Computer's Mouse event handler """
        try:
            server = self.get_server()
            clients = server.clients
            if self.__active_computer_position != self.__position:   # Mouse is not on current computer
                x, y = event.Position
                if event.MessageName == "mouse move":
                    value = self.get_mouse_movement(x, y).__dict__
                    event = Event(Event.MOVE_MOUSE, value)
                elif event.MessageName == "mouse left up":
                    event = Event(Event.MOUSE_LEFT_UP)
                elif event.MessageName == "mouse left down":
                    event = Event(Event.MOUSE_LEFT_DOWN)
                elif event.MessageName == "mouse right up":
                    event = Event(Event.MOUSE_RIGHT_UP)
                elif event.MessageName == "mouse right down":
                    event = Event(Event.MOUSE_RIGHT_DOWN)
                elif event.MessageName == "mouse wheel":
                    event = Event(Event.MOUSE_WHEEL, value=str(event.Wheel))
                else:
                    return False    # Maybe make it true in this case to be mouse back to main screen
                active_computer_client = self.get_active_computer_client()
                if active_computer_client is not None:
                    server.send_event(active_computer_client, event)
                    logging.debug(f"Mouse is on some other computer {self.__active_computer_position}")
                else:
                    self.__active_computer_position = self.__position
                return False

            if event.Position[0] > self.__width - 1:    # 0 is position X
                if len(clients) > 0:  # Client is connected
                    self.__active_computer_position = self.__position + 1

                    active_computer_client = self.get_active_computer_client()
                    event = Event(Event.CLIPBOARD, OS.get_clipboard_data())
                    server.send_event(active_computer_client, event)
                    logging.info(f"Switch to computer {self.__active_computer_position}")

            return True
        except Exception as e:
            logging.exception(e)
            return True

    def keyboard_handler(self, event):
        """ Computer's Keyboard event handler """
        try:
            server = self.get_server()
            # clients = server.clients
            if self.__active_computer_position != self.__position:  # Mouse is not on current computer
                value = event.KeyID
                if event.MessageName == "key down":
                    event = Event(Event.KEY_DOWN, value)
                elif event.MessageName == "key up":
                    event = Event(Event.KEY_UP, value)
                else:
                    return False    # Maybe make it true in this case to be mouse back to main screen

                active_computer_client = self.get_active_computer_client()
                if active_computer_client is not None:
                    server.send_event(active_computer_client, event)
                    logging.debug(f"Mouse is on some other computer {self.__active_computer_position}")
                else:
                    self.__active_computer_position = self.__position
                return False

            return True
        except Exception as e:
            logging.exception(e)
            return True
