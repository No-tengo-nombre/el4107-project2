from camsv.configs import RECEIVING_WINDOW


def handle_user(user_conn, camera_socket):
    recv_packet = camera_socket.recv(RECEIVING_WINDOW)
    user_conn.send(recv_packet)
