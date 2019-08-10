"""
    DeskUnity
"""


class Event:
    TEST = "TEST"
    CONNECTION_TEST = "CONNECTION_TEST"
    MOVE_MOUSE = "MOVE_MOUSE"
    MOUSE_LEFT_DOWN = "MOUSE_LEFT_DOWN"
    MOUSE_LEFT_UP = "MOUSE_LEFT_UP"
    MOUSE_RIGHT_DOWN = "MOUSE_RIGHT_DOWN"
    MOUSE_RIGHT_UP = "MOUSE_RIGHT_UP"
    MOUSE_WHEEL = "MOUSE_WHEEL"
    KEY_UP = "KEY_UP"
    KEY_DOWN = "KEY_DOWN"
    CLIPBOARD = "CLIPBOARD"
    CHANGE_POSITION = "CHANGE_POSITION"
    SERVER_SHUT = "SERVER_SHUT"

    def __init__(self, name, value="", client=None, computer=None):
        self.name = name
        self.value = value
        self.client = client
        self.computer = computer
