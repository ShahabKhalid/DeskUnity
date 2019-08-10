"""
    DeskUnity v1.0
    Event Data Encoder
"""
import json
import logging

from core.event import Event
from Configs import ENCODE_FORMAT, EVENT_SEPARATOR


class EventEncoder:

    @staticmethod
    def decode(event):
        if not isinstance(event, str):
            raise Exception("Invalid json string passed.")
        try:
            event = event.replace("\"", "\\\"")
            event = event.replace("\'", "\"")
            json_ = json.loads(event)
            value = json_["value"] if json_["value"] else ""
            return Event(json_["name"], value)
        except (json.decoder.JSONDecodeError, KeyError) as e:
            logging.error("Invalid event passed. " + event)
            logging.exception(e)
        except Exception as e:
            logging.error("Unknown issue happened.")
            logging.exception(e)

    @staticmethod
    def encode(event):
        # Todo: Encrypt messages
        if not isinstance(event, Event):
            logging.error("Argument passed is not an event.")
        event = event.__dict__
        del event['client']
        del event['computer']
        return (str(event)+EVENT_SEPARATOR).encode(ENCODE_FORMAT)
