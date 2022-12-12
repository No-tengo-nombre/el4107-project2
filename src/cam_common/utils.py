from cam_common.configs import RECEIVING_WINDOW


def receive_full_msg(sock, window=RECEIVING_WINDOW):
    while True:
        msg = sock.recv(window).decode()
        if msg == "":
            break
        yield msg
