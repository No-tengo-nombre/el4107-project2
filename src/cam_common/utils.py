import socket

from cam_common.configs import RECEIVING_WINDOW, SIZE_RECEIVING_WINDOW
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
    recv_size = 0
    while recv_size < msg_size:
        try:
            msg = sock.recv(window)
            if msg.endswith(br"\r\n"):
                recv_size = msg_size
            else:
                recv_size += window
            yield msg
        except socket.timeout:
            LOGGER.warning("Receiving timeout")


def receive_full_msg(sock, size_window=SIZE_RECEIVING_WINDOW, window=RECEIVING_WINDOW):
    # msg_size = int(sock.recv(size_window).decode())
    # LOGGER.debug(f"Received message size {msg_size}")
    # final_msg = b""
    # for part in yield_full_msg(sock, msg_size, window):
    #     final_msg += part
    # LOGGER.debug(f"Received message {final_msg}")
    # return final_msg

    final_msg = b""
    while True:
        msg = sock.recv(window)
        final_msg += msg
        if msg.endswith(rb"\r\n\r\n"):
            break
    LOGGER.debug(f"Received message {final_msg}")
    return final_msg


def send_full_msg(sock, message, size_window=SIZE_RECEIVING_WINDOW):
    """Send the message size and message, assumming the input is already encoded."""
    # msg_size = len(message)
    # sock.send(str(msg_size).zfill(size_window).encode())
    # sock.send(message)

    if message.endswith(rb"\r\n\r\n"):
        sock.send(message)
    else:
        sock.send(message + br"\r\n\r\n")
