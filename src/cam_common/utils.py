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


def yield_full_msg(sock, msg_size, window=RECEIVING_WINDOW):
    # while True:
    #     try:
    #         msg = sock.recv(window)
    #         if msg == b"":
    #             break
    #         yield msg
    #     except socket.timeout:
    #         LOGGER.warning("Receiving timeout")

    recv_size = 0
    while recv_size < msg_size:
        try:
            msg = sock.recv(window)
            recv_size += window
            yield msg
        except socket.timeout:
            LOGGER.warning("Receiving timeout")


def receive_full_msg(sock, window=RECEIVING_WINDOW):
    # final_msg = b""
    # for part in yield_full_msg(sock, window):
    #     print(part)
    #     final_msg += part
    # print("SDFSFSDF")
    # return final_msg

    msg_size = int(sock.recv(window).decode())
    final_msg = b""
    for part in yield_full_msg(sock, msg_size, window):
        final_msg += part
    return final_msg


def send_full_msg(sock, message, window=RECEIVING_WINDOW):
    """Send the message size and message, assumming the input is already encoded."""
    msg_size = len(message)
    sock.send(str(msg_size).encode())
    sock.send(message)
