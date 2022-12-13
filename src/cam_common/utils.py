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
    finished = False
    while not finished:
        try:
            msg = sock.recv(window)
            if msg.endswith(rb"\r\n\r\n"):
                finished = True
                yield msg[:-8]
            else:
                yield msg
        except socket.timeout:
            LOGGER.warning("Receiving timeout")


def receive_full_msg(sock, window=RECEIVING_WINDOW):
    final_msg = b"".join(yield_full_msg(sock, window))
    LOGGER.debug(f"Received message {final_msg}")
    return final_msg


def send_full_msg(sock, message):
    if message.endswith(rb"\r\n\r\n"):
        sock.send(message)
    else:
        sock.send(message + br"\r\n\r\n")
