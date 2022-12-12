from cam_common.configs import RECEIVING_WINDOW


def yield_full_msg(sock, window=RECEIVING_WINDOW):
    while True:
        msg = sock.recv(window)
        if msg == b"":
            break
        yield msg


def receive_full_msg(sock, window=RECEIVING_WINDOW):
    final_msg = b""
    for part in yield_full_msg(sock, window):
        final_msg += part
    return final_msg
