import socket
import threading

from cam_common.configs import DEFAULT_SERVER_PORT, DEFAULT_CLIENT_PORT, DEFAULT_TIMEOUT
from cam_common.logger import LOGGER
from cam_common.utils import receive_full_msg, EMPTY_SOCKET, send_full_msg
from cam_server.core.user_handle import handle_user
from cam_server.database.database import USER_DATABASE
from cam_server.core.resource_assigner import PortAssigner


# WELCOME_MSG = r"""
#   ______                         ______           __ __ __     
#  /      \                       /      \         |  \  \  \    
# |  ▓▓▓▓▓▓\ ______  ______ ____ |  ▓▓▓▓▓▓\ ______  \▓▓ ▓▓ ▓▓
# | ▓▓   \▓▓|      \|      \    \| ▓▓ __\▓▓/      \|  \ ▓▓ ▓▓
# | ▓▓       \▓▓▓▓▓▓\ ▓▓▓▓▓▓\▓▓▓▓\ ▓▓|    \  ▓▓▓▓▓▓\ ▓▓ ▓▓ ▓▓
# | ▓▓   __ /      ▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓ \▓▓▓▓ ▓▓   \▓▓ ▓▓ ▓▓ ▓▓
# | ▓▓__/  \  ▓▓▓▓▓▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓__| ▓▓ ▓▓     | ▓▓ ▓▓ ▓▓
#  \▓▓    ▓▓\▓▓    ▓▓ ▓▓ | ▓▓ | ▓▓\▓▓    ▓▓ ▓▓     | ▓▓ ▓▓ ▓▓
#   \▓▓▓▓▓▓  \▓▓▓▓▓▓▓\▓▓  \▓▓  \▓▓ \▓▓▓▓▓▓ \▓▓      \▓▓\▓▓\▓▓
          
#           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣷⣶⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀
#           ⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡟⠁⣰⣿⣿⣿⡿⠿⠻⠿⣿⣿⣿⣿⣧⠀⠀⠀⠀
#           ⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠏⠀⣴⣿⣿⣿⠉⠀⠀⠀⠀⠀⠈⢻⣿⣿⣇⠀⠀⠀
#           ⠀⠀⠀⠀⢀⣠⣼⣿⣿⡏⠀⢠⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡀⠀⠀
#           ⠀⠀⠀⣰⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀
#           ⠀⠀⢰⣿⣿⡿⣿⣿⣿⡇⠀⠘⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⣿⠁⠀⠀
#           ⠀⠀⣿⣿⣿⠁⣿⣿⣿⡇⠀⠀⠻⣿⣿⣿⣷⣶⣶⣶⣶⣶⣿⣿⣿⣿⠃⠀⠀⠀
#           ⠀⢰⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
#           ⠀⢸⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⢉⣿⣿⠀⠀⠀⠀⠀⠀
#           ⠀⢸⣿⣿⣇⠀⣿⣿⣿⠀⠀⠀⠀⠀⢀⣤⣤⣤⡀⠀⠀⢸⣿⣿⣿⣷⣦⠀⠀⠀
#           ⠀⠀⢻⣿⣿⣶⣿⣿⣿⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣦⡀⠀⠉⠉⠻⣿⣿⡇⠀⠀
#           ⠀⠀⠀⠛⠿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠈⠹⣿⣿⣇⣀⠀⣠⣾⣿⣿⡇⠀⠀
#           ⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣦⣤⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
#           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⠿⠋⠉⠛⠋⠉⠉⠁⠀⠀⠀⠀
#           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁

# """
WELCOME_MSG = r"""
hello uwu

"""


class ServerCore:
    db = USER_DATABASE

    def __init__(self, ip="", port=DEFAULT_SERVER_PORT, client_port=DEFAULT_CLIENT_PORT, timeout=DEFAULT_TIMEOUT):
        self.__should_close = False
        self._ip = ip
        self._port = port
        self._client_port = client_port
        self._desc = (self.ip, self.port)
        self._timeout = timeout
        self.__client_socket = EMPTY_SOCKET
        self.__user_recv_socket = EMPTY_SOCKET
        self.__user_socket = EMPTY_SOCKET

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def client_port(self):
        return self._client_port

    @property
    def desc(self):
        return self._desc

    @property
    def timeout(self):
        return self._timeout

    @ip.setter
    def ip(self, new_ip):
        self._ip = new_ip
        self._desc = (new_ip, self.port)

    @port.setter
    def port(self, new_port):
        self._port = new_port
        self._desc = (self.ip, new_port)

    @client_port.setter
    def client_port(self, new_port):
        self._client_port = new_port

    @desc.setter
    def desc(self, new_desc):
        self._desc = new_desc
        self._ip, self._port = new_desc

    @timeout.setter
    def timeout(self, new_timeout):
        self._timeout = new_timeout
        # self.__client_socket.settimeout(new_timeout)
        # self.__user_recv_socket.settimeout(new_timeout)
        # self.__user_socket.settimeout(new_timeout)

    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
                self.__client_socket = client_s
                # client_s.settimeout(self.timeout)

                # Leave the IP blank to receive from public IP
                client_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                client_s.bind((self.ip, self.client_port))

                # Receive the client connection
                client_s.listen()
                LOGGER.info("Waiting for client connection")
                client_conn, client_addr = client_s.accept()
                LOGGER.info(f"Connection with client {client_addr} accepted")

                while not self.__should_close:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as user_recv_s:
                        self.__user_recv_socket = user_recv_s
                        # user_recv_s.settimeout(self.timeout)

                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as user_s:
                            self.__user_socket = user_s
                            # user_s.settimeout(self.timeout)

                            # Leave the IP blank to receive from public IP
                            user_recv_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            user_recv_s.bind((self.ip, self.port))

                            # Receive the initial user connection
                            user_recv_s.listen()
                            LOGGER.info(f"Waiting for a user connection, socket {user_recv_s}")
                            conn, addr = user_recv_s.accept()
                            LOGGER.info(f"Connection with {conn} accepted")

                            # Redirect the connection to another port
                            port = PortAssigner.get_port()
                            try:
                                user_s.bind((self.ip, port))
                                user_s.listen()
                                # conn.send(f"@redirect_port {port}".encode())
                                send_full_msg(conn, f"@redirect_port {port}".encode())
                                # conn.recv(RECEIVING_WINDOW)
                                receive_full_msg(conn)
                                LOGGER.info("Received port redirection OK")

                                # Accept the connection to the new port
                                conn, addr = user_s.accept()
                                LOGGER.info(f"Assigned {addr} to port {port}")
                                # conn.send(WELCOME_MSG.encode())
                                send_full_msg(conn, WELCOME_MSG.encode())

                                user_thread = threading.Thread(target=handle_user, args=(self, self.db, conn, user_s, client_conn, client_s, port))
                                user_thread.start()
                            except Exception as e:
                                LOGGER.warning(f"Error assigning user to port {port}, found exception {e}")

        except Exception as e:
            LOGGER.warning(f"Closing server, found exception {e}")
            self.close()

        finally:
            self.clean_up()

    def close(self):
        self.__should_close = True

    def clean_up(self):
        pass
