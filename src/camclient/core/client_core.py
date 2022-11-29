import socket

from camcommon import FIXED_SERVER_DESC
from camcommon.logger import LOGGER
from camclient.core.packet_handle import handle_packet


class ClientCore:
    def __init__(self):
        self.__should_close = False

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(FIXED_SERVER_DESC)
            s.listen()

            while not self.__should_close:
                conn, addr = s.accept()
                LOGGER.info(f"Connection accepted from {addr}")

                packet = conn.recv(1024)
                handle_packet()
