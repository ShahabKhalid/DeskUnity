""""
    DeskUnity
"""
try:
    import pyHook3 as pyHook
except ImportError:
    import pyHook
import logging
import threading
import pythoncom


class Hook:

    def __init__(self, mouse_handler=None, keyboard_handler=None):
        self.__hook_manager = pyHook.HookManager()
        self.__mouse_handler = mouse_handler
        self.__keyboard_handler = keyboard_handler
        self.__mouse_hooked = False
        self.__keyboard_hooked = False

    def set_mouse_handler(self, mouse_handler):
        self.__mouse_handler = mouse_handler

    def get_mouse_handler(self):
        return self.__mouse_handler

    def set_keyboard_handler(self, keyboard_handler):
        self.__keyboard_handler = keyboard_handler

    def get_keyboard_handler(self):
        return self.__keyboard_handler

    def mouse_manager(self, event):
        try:
            # logging.debug(f'MessageName: {event.MessageName}')
            # logging.debug(f'Position: {event.Position}')
            # logging.debug(f'Wheel: {event.Wheel}')
            # logging.debug(f'Message: {event.Message}')
            # logging.debug(f'Time: {event.Time}')
            # logging.debug(f'Window: {event.Window}')
            # logging.debug(f'WindowName: {event.WindowName}')
            # logging.debug(f'Injected: {event.Injected}')
            if self.__mouse_handler:
                return self.__mouse_handler(event)
            return True
        except Exception as e:
            logging.exception(e)
            return True
        
    def key_manager(self, event):
        try:
            # logging.debug(f'MessageName: {event.MessageName}')
            # logging.debug(f'Message: {event.Message}')
            # logging.debug(f'Time: {event.Time}')
            # logging.debug(f'Window: {event.Window}')
            # logging.debug(f'WindowName: {event.WindowName}')
            # logging.debug(f'Ascii: {event.Ascii, chr(event.Ascii)}')
            # logging.debug(f'Key: {event.Key}')
            # logging.debug(f'KeyID: {event.KeyID}')
            # logging.debug(f'ScanCode: {event.ScanCode}')
            # logging.debug(f'Extended: {event.Extended}')
            # logging.debug(f'Injected: {event.Injected}')
            # logging.debug(f'Alt {event.Alt}')
            # logging.debug(f'Transition {event.Transition}')
            if self.__keyboard_handler:
                return self.__keyboard_handler(event)
            return True
        except Exception as e:
            logging.exception(e)
            return True

    def hook_mouse(self):
        self.__mouse_hooked = True

        def hook():
            self.__hook_manager.MouseAll = self.mouse_manager
            self.__hook_manager.HookMouse()
            while self.__mouse_hooked:
                pythoncom.PumpWaitingMessages()
        threading.Thread(target=hook).start()

    def unhook_mouse(self):
        self.__mouse_hooked = False
        self.__hook_manager.UnhookMouse()

    def hook_keyboard(self):
        self.__keyboard_hooked = True

        def hook():
            self.__hook_manager.KeyAll = self.key_manager
            self.__hook_manager.HookKeyboard()
            while self.__keyboard_hooked:
                pythoncom.PumpWaitingMessages()
        threading.Thread(target=hook).start()

    def unhook_keyboard(self):
        self.__keyboard_hooked = False
        self.__hook_manager.UnhookKeyboard()

