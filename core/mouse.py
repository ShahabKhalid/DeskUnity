"""
    DeskUnity
"""
from pynput.mouse import Controller, Button


class Mouse:
    mouse = Controller()

    @staticmethod
    def move(x, y):
        Mouse.mouse.move(x, y)

    @staticmethod
    def get_position():
        return Mouse.mouse.position
