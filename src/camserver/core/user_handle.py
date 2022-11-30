from camcommon import RECEIVING_WINDOW, END_AUTH_STRING
from camcommon.logger import LOGGER
from camserver.database.database import UserNotFoundException


def handle_user(db, user_conn, user_socket, camera_socket):
    if validate_user(db, user_conn):
        LOGGER.info("Successfuly validated user.")
        user_conn.send("Successfuly validated user.".encode())
        recv_packet = camera_socket.recv(RECEIVING_WINDOW)
        user_conn.send(recv_packet)
    else:
        LOGGER.info("Failed to validate user.")
        user_conn.send(END_AUTH_STRING.encode())

        user_conn.send("Failed to validate user.".encode())
        user_socket.close()
        LOGGER.info("Finishing user thread.")


def validate_user(db, conn):
    conn.send("Enter username: ".encode())
    username = conn.recv(1024).decode()
    LOGGER.info(f"Received username {username}")

    conn.send("Enter password: ".encode())
    password = conn.recv(1024).decode()
    LOGGER.info(f"Received password {password}")

    try:
        validation_status = db.validate_user(username, password)
        LOGGER.info(f"Validation status {validation_status}.")
        return validation_status
    except UserNotFoundException:
        conn.send(f"User {username} was not found, would you like to create it? (y/n): ".encode())
        answer = conn.recv(1024).decode().upper()
        if answer == "Y":
            db.register_user(username, password)
            conn.send(f"Registered user {username}. Welcome!".encode())
            return True
        else:
            return False
