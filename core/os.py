"""
    DeskUnity
    OS Class
"""
from tkinter import Tk
import pyperclip


class OS:
    WINDOWS = "WINDOWS"
    LINUX = "LINUX"
    OSX = "OSX"

    __CURRENT_OS = WINDOWS

    @staticmethod
    def define(os):
        if os != OS.WINDOWS or os != OS.LINUX or os != OS.OSX:
            raise Exception("Undefined OS, Should be [{},{},{}]".format(OS.WINDOWS, OS.LINUX, OS.OSX))
        else:
            OS.__CURRENT_OS = os

    @staticmethod
    def get():
        """ Returns OS """
        return OS.__CURRENT_OS

    @staticmethod
    def get_clipboard_data():
        return pyperclip.paste()

    @staticmethod
    def set_clipboard_data(data):
        pyperclip.copy(data)
