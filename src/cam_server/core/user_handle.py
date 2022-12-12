from cam_common.configs import USER_LOCAL_PORT
from cam_common.logger import LOGGER
from cam_common.requests import get_request_field, replace_request_field
from cam_common.utils import receive_full_msg, send_full_msg
from cam_server.database.database import UserNotFoundException
from cam_server.core.resource_assigner import PortAssigner

import time


def handle_user(
    server, db, user_conn, user_socket, client_conn, client_socket, user_port
):
    try:
        time.sleep(1)
        if validate_user(db, user_conn):
            LOGGER.info("Successfuly validated user")
            send_full_msg(user_conn, "@echo Successfuly validated user :)".encode())
            receive_full_msg(user_conn)
            send_full_msg(user_conn, "@break_while_loop".encode())
            receive_full_msg(user_conn)

            handle_user_flow(
                server, user_conn, user_socket, client_conn, client_socket, user_port
            )
        else:
            LOGGER.info("Failed to validate user")
            send_full_msg(user_conn, "@kick Failed to validate the user :(".encode())

            user_socket.close()
            PortAssigner.release_port(user_port)
            LOGGER.info("Finishing user thread.")
    except Exception as e:
        LOGGER.warning(
            f"Connection with user {user_conn} suddenly closed, found exception {e}"
        )
    finally:
        PortAssigner.release_port(user_port)


def handle_user_flow(
    server, user_conn, user_socket, client_conn, client_socket, user_port
):
    LOGGER.info(f"Sending connection request")
    send_full_msg(user_conn, f"@webbrowser_new_tab http:// 127.0.0.1 {USER_LOCAL_PORT}".encode())
    LOGGER.info("Receiving connection request confirmation")
    receive_full_msg(user_conn)

    LOGGER.info("Received confirmation, moving to packet redirection")
    time.sleep(1)
    while True:
        LOGGER.debug("Listening for user packet")
        packet = receive_full_msg(user_conn)
        try:
            user_addr = get_request_field(packet, "Host")
            packet = replace_request_field(packet, "Host", f"{server.ip}:{user_port}")
            LOGGER.debug(f"Replaced field Host in user packet, got {packet}")
        except:
            LOGGER.info("Request does not contain field Host")
        try:
            user_referer = get_request_field(packet, "Referer")
            packet = replace_request_field(packet, "Referer", f"http://{server.ip}:{user_port}/")
            LOGGER.debug(f"Replaced field Referer in user packet, got {packet}")
        except:
            LOGGER.info("Request does not contain field Referer")

        LOGGER.debug("Sending packet to client")
        send_full_msg(client_conn, packet)

        LOGGER.debug("Listening for client packet")
        response = receive_full_msg(client_conn)
        try:
            response = replace_request_field(response, "Host", user_addr)
            LOGGER.debug(f"Replaced field Host in client response, got {response}")
        except:
            LOGGER.info("Request does not contain field Host")
        try:
            response = replace_request_field(response, "Referer", user_referer)
            LOGGER.debug(f"Replaced field Referer in client response, got {response}")
        except:
            LOGGER.info("Request does not contain field Referer")

        LOGGER.debug("Sending packet to user")
        send_full_msg(user_conn, response)


def validate_user(db, conn):
    send_full_msg(conn, "@input Enter username".encode())
    username = receive_full_msg(conn).decode()
    LOGGER.info(f"Received username {username}")

    send_full_msg(conn, "@hidden_input Enter password".encode())
    password = receive_full_msg(conn).decode()
    LOGGER.info("Received password")

    try:
        validation_status = db.validate_user(username, password)
        LOGGER.info(f"Validation status {validation_status}")
        time.sleep(1)
        return validation_status
    except UserNotFoundException:
        send_full_msg(
            conn,
            f"@input User {username} was not found, would you like to create it? (y/n)".encode(),
        )
        answer = receive_full_msg(conn).decode().upper()
        if answer == "Y":
            db.register_user(username, password)
            send_full_msg(conn, f"@echo Registered user {username}. Welcome!".encode())
            time.sleep(1)
            return True
        else:
            time.sleep(1)
            return False
