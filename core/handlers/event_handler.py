"""
    DeskUnity
"""
import logging

from core.event import Event
from core.mouse import Mouse, Button
from core.keyboard import KeyBoard, KeyCode
from Configs import MOUSE_SCROLL_SPEED
from core.os import OS


class EventHandler:

    @staticmethod
    def handle(event):
        """ Event responder / handler """
        try:
            if not isinstance(event, Event):
                raise Exception("Invalid event passed")

            logging.debug(f"Received Event: {event.name}")
            if event.name == Event.CONNECTION_TEST:
                event.client.connection.close()

            elif event.name == Event.MOVE_MOUSE:
                Mouse.move(event.value['x'], event.value['y'])
                x, y = Mouse.get_position()
                if x < 1:
                    event_clipboard = Event(Event.CLIPBOARD, value=OS.get_clipboard_data(), client=event.client)
                    event_clipboard.client.send_event(event_clipboard)
                    event = Event(Event.CHANGE_POSITION, value=str(event.computer.get_position() - 1),
                                  client=event.client)
                    event.client.send_event(event)

            elif event.name == Event.CHANGE_POSITION:
                event.computer.set_active_computer_position(int(event.value))

            elif event.name == Event.MOUSE_LEFT_DOWN:
                Mouse.mouse.press(Button.left)

            elif event.name == Event.MOUSE_RIGHT_DOWN:
                Mouse.mouse.press(Button.right)

            elif event.name == Event.MOUSE_LEFT_UP:
                Mouse.mouse.release(Button.left)

            elif event.name == Event.MOUSE_RIGHT_UP:
                Mouse.mouse.release(Button.right)

            elif event.name == Event.MOUSE_WHEEL:
                Mouse.mouse.scroll(0, int(event.value) * MOUSE_SCROLL_SPEED)

            elif event.name == Event.KEY_DOWN:
                KeyBoard.keyboard.press(KeyCode.from_vk(event.value))

            elif event.name == Event.KEY_UP:
                KeyBoard.keyboard.release(KeyCode.from_vk(event.value))

            elif event.name == Event.CLIPBOARD:
                OS.set_clipboard_data(event.value)

        except Exception as e:
            logging.error("Error while handling event.")
            logging.exception(e)
