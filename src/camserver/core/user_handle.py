from camcommon import RECEIVING_WINDOW
from camcommon.logger import LOGGER
from camserver.database.database import UserNotFoundException


def handle_user(db, user_conn, user_socket, camera_socket):
    if validate_user(db, user_conn):
        user_conn.send("Successfuly validated user.".encode())
        recv_packet = camera_socket.recv(RECEIVING_WINDOW)
        user_conn.send(recv_packet)
    else:
        user_conn.send("Failed to validate user.".encode())


def validate_user(db, conn):
    conn.send("Enter username: ".encode())
    username = conn.recv(1024).decode()
    LOGGER.info(f"Received username {username}")

    conn.send("Enter password: ".encode())
    password = conn.recv(1024).decode()
    LOGGER.info(f"Received password {password}")

    try:
        return db.validate_user(username, password)
    except UserNotFoundException:
        conn.send(f"User {username} was not found, would you like to create it? (y/n)".encode())
        answer = conn.recv(1024).decode().upper()
        if answer == "Y":
            db.register_user(username, password)
            conn.send(f"Registered user {username}. Welcome!".encode())
            return True
        else:
            return False
