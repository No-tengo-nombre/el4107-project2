import socket

from camcommon import FIXED_SERVER_DESC, RECEIVING_WINDOW
from camclient.core.packet_handle import handle_packet, handle_auth


class ClientCore:
    def __init__(self):
        self.__should_close = False

    def close(self):
        self.__should_close = True

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(FIXED_SERVER_DESC)
            welcome_msg = s.recv(RECEIVING_WINDOW)
            print(welcome_msg.decode())

            handle_auth(s)
            while not self.__should_close:
                packet = s.recv(RECEIVING_WINDOW)
                handle_packet(packet, self)
