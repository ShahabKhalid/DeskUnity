""""
    DeskUnity v1.0
    Main File
"""
import time
from core.deskunity import DeskUnity

# Todo : I left here :: Write Mouse event listener, send it to all active computer
if __name__ == "__main__":
    desk_unity = DeskUnity()
    server = desk_unity.start()
    desk_unity.show_ui()

    # Client don't send mouse event right now so lets keep the client running with a loop
    # Todo: Client can also send his mouse event to control server or other clients
