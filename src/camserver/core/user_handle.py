from camcommon import RECEIVING_WINDOW


def handle_user(user_conn, user_socket, camera_socket):
    validate_user(user_conn)

    recv_packet = camera_socket.recv(RECEIVING_WINDOW)
    user_conn.send(recv_packet)


def validate_user(conn):
    conn.send("Enter username: ".encode())
    username = conn.recv(1024).decode()
    conn.send("Enter password: ".encode())
    password = conn.recv(1024).decode()
