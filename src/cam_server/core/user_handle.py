from cam_common.configs import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, RECEIVING_WINDOW
from cam_common.logger import LOGGER
from cam_common.utils import receive_full_msg, send_full_msg
from cam_server.database.database import UserNotFoundException
from cam_server.core.resource_assigner import PortAssigner

import time
import webbrowser


def handle_user(server, db, user_conn, user_socket, client_conn, client_socket, user_port):
    try:
        time.sleep(1)
        if validate_user(db, user_conn):
            LOGGER.info("Successfuly validated user")
            # user_conn.send("@echo Successfuly validated user :)".encode())
            send_full_msg(user_conn, "@echo Successfuly validated user :)".encode())
            # user_conn.recv(RECEIVING_WINDOW)
            receive_full_msg(user_conn)
            # user_conn.send("@break_while_loop".encode())
            send_full_msg(user_conn, "@break_while_loop".encode())
            # user_conn.recv(RECEIVING_WINDOW)
            receive_full_msg(user_conn)

            handle_user_flow(server, user_conn, user_socket, client_conn, client_socket, user_port)
        else:
            LOGGER.info("Failed to validate user")
            # user_conn.send("@kick Failed to validate the user :(".encode())
            send_full_msg(user_conn, "@kick Failed to validate the user :(".encode())

            user_socket.close()
            PortAssigner.release_port(user_port)
            LOGGER.info("Finishing user thread.")
    except Exception as e:
        LOGGER.warning(f"Connection with user {user_conn} suddenly closed, found exception {e}")
    finally:
        PortAssigner.release_port(user_port)


def handle_user_flow(server, user_conn, user_socket, client_conn, client_socket, user_port):
    LOGGER.info(f"Sending connection request")
    # user_conn.send(f"@webbrowser_new_tab http:// $ip {user_port}".encode())
    send_full_msg(user_conn, f"@webbrowser_new_tab http:// $ip {user_port}".encode())
    LOGGER.info("Receiving connection request confirmation")
    # user_conn.recv(RECEIVING_WINDOW)
    receive_full_msg(user_conn)

    LOGGER.info("Received confirmation, moving to packet redirection")
    while True:
        LOGGER.debug("Listening for user packet")
        # packet = user_conn.recv(RECEIVING_WINDOW)
        packet = receive_full_msg(user_conn)
        print("RECEIVED PACKETAS DFSAF SAD FSDF SD")
        print(packet.decode())
        LOGGER.debug("Sending packet to client")
        # client_conn.send(packet)
        send_full_msg(client_conn, packet)
        LOGGER.debug("Listening for client packet")
        # response = client_conn.recv(RECEIVING_WINDOW)
        response = receive_full_msg(client_conn)
        LOGGER.debug("Sending packet to user")
        # user_conn.send(response)
        send_full_msg(user_conn, response)


def validate_user(db, conn):
    # conn.send("@input Enter username".encode())
    send_full_msg(conn, "@input Enter username".encode())
    # username = conn.recv(RECEIVING_WINDOW).decode()
    username = receive_full_msg(conn).decode()
    LOGGER.info(f"Received username {username}")

    # conn.send("@hidden_input Enter password".encode())
    send_full_msg(conn, "@hidden_input Enter password".encode())
    # password = conn.recv(RECEIVING_WINDOW).decode()
    password = receive_full_msg(conn).decode()
    LOGGER.info("Received password")

    try:
        validation_status = db.validate_user(username, password)
        LOGGER.info(f"Validation status {validation_status}")
        return validation_status
    except UserNotFoundException:
        # conn.send(f"@input User {username} was not found, would you like to create it? (y/n): ".encode())
        send_full_msg(conn, f"@input User {username} was not found, would you like to create it? (y/n): ".encode())
        # answer = conn.recv(RECEIVING_WINDOW).decode().upper()
        answer = receive_full_msg(conn).decode().upper()
        if answer == "Y":
            db.register_user(username, password)
            # conn.send(f"@echo Registered user {username}. Welcome!".encode())
            send_full_msg(conn, f"@echo Registered user {username}. Welcome!".encode())
            return True
        else:
            return False
