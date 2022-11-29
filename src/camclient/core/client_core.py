import socket

from camcommon import FIXED_SERVER_PORT, FIXED_SERVER_DESC, RECEIVING_WINDOW
from camcommon.logger import LOGGER
from camclient.core.packet_handle import handle_packet


class ClientCore:
    def __init__(self):
        self.__should_close = False

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(FIXED_SERVER_DESC)

            while not self.__should_close:
                packet = s.recv(RECEIVING_WINDOW)
                handle_packet(packet)
