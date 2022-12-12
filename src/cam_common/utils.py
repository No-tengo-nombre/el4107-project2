import socket

from cam_common.configs import RECEIVING_WINDOW
from cam_common.logger import LOGGER


class EMPTY_SOCKET:
    @staticmethod
    def settimeout(*_):
        pass

    @staticmethod
    def recv(*_):
        pass

    @staticmethod
    def send(*_):
        pass


def yield_full_msg(sock, window=RECEIVING_WINDOW):
    while True:
        try:
            msg = sock.recv(window)
            if msg == b"":
                break
            yield msg
        except socket.timeout:
            LOGGER.warning("Receiving timeout")


def receive_full_msg(sock, window=RECEIVING_WINDOW):
    final_msg = b""
    for part in yield_full_msg(sock, window):
        print(part)
        final_msg += part
    print("SDFSFSDF")
    return final_msg
