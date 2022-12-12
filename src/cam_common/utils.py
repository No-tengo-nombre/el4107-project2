from cam_common.configs import RECEIVING_WINDOW


def yield_full_msg(sock, window=RECEIVING_WINDOW):
    while True:
        msg = sock.recv(window).decode()
        if msg == "":
            break
        yield msg


def receive_full_msg(sock, window=RECEIVING_WINDOW):
    final_msg = ""
    for part in yield_full_msg(sock, window):
        final_msg += part
    return final_msg
