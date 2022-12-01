from cam_common import RECEIVING_WINDOW
from cam_common.logger import LOGGER
from cam_server.database.database import UserNotFoundException
from cam_server.core.resource_assigner import PortAssigner


def handle_user(db, user_conn, user_socket, camera_socket, user_port):
    try:
        if validate_user(db, user_conn):
            LOGGER.info("Successfuly validated user")
            user_conn.send("@echo Successfuly validated user :)".encode())
            user_conn.send("@break_while_loop".encode())

            handle_user_flow()
        else:
            LOGGER.info("Failed to validate user")
            user_conn.send("@kick Failed to validate the user :(".encode())

            user_socket.close()
            PortAssigner.release_port(user_port)
            LOGGER.info("Finishing user thread.")
    except:
        LOGGER.warning(f"Connection with user {user_conn} suddenly closed.")
    finally:
        PortAssigner.release_port(user_port)


def handle_user_flow():
    pass


def validate_user(db, conn):
    conn.send("@input Enter username".encode())
    username = conn.recv(1024).decode()
    LOGGER.info(f"Received username {username}")

    conn.send("@hidden_input Enter password".encode())
    password = conn.recv(1024).decode()
    LOGGER.info(f"Received password {password}")

    try:
        validation_status = db.validate_user(username, password)
        LOGGER.info(f"Validation status {validation_status}")
        return validation_status
    except UserNotFoundException:
        conn.send(f"@input User {username} was not found, would you like to create it? (y/n): ".encode())
        answer = conn.recv(1024).decode().upper()
        if answer == "Y":
            db.register_user(username, password)
            conn.send(f"@echo Registered user {username}. Welcome!".encode())
            return True
        else:
            return False
