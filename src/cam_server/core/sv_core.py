import socket
import threading

from cam_common import FIXED_CAMERA_DESC, FIXED_SERVER_IP, FIXED_SERVER_PORT, FIXED_SERVER_DESC
from cam_common.logger import LOGGER
from cam_server.core.user_handle import handle_user
from cam_server.database.database import USER_DATABASE
from cam_server.core.resource_assigner import PortAssigner


WELCOME_MSG = r"""
  ______                         ______           __ __ __     
 /      \                       /      \         |  \  \  \    
|  ▓▓▓▓▓▓\ ______  ______ ____ |  ▓▓▓▓▓▓\ ______  \▓▓ ▓▓ ▓▓
| ▓▓   \▓▓|      \|      \    \| ▓▓ __\▓▓/      \|  \ ▓▓ ▓▓
| ▓▓       \▓▓▓▓▓▓\ ▓▓▓▓▓▓\▓▓▓▓\ ▓▓|    \  ▓▓▓▓▓▓\ ▓▓ ▓▓ ▓▓
| ▓▓   __ /      ▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓ \▓▓▓▓ ▓▓   \▓▓ ▓▓ ▓▓ ▓▓
| ▓▓__/  \  ▓▓▓▓▓▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓__| ▓▓ ▓▓     | ▓▓ ▓▓ ▓▓
 \▓▓    ▓▓\▓▓    ▓▓ ▓▓ | ▓▓ | ▓▓\▓▓    ▓▓ ▓▓     | ▓▓ ▓▓ ▓▓
  \▓▓▓▓▓▓  \▓▓▓▓▓▓▓\▓▓  \▓▓  \▓▓ \▓▓▓▓▓▓ \▓▓      \▓▓\▓▓\▓▓
          
          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣷⣶⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡟⠁⣰⣿⣿⣿⡿⠿⠻⠿⣿⣿⣿⣿⣧⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠏⠀⣴⣿⣿⣿⠉⠀⠀⠀⠀⠀⠈⢻⣿⣿⣇⠀⠀⠀
          ⠀⠀⠀⠀⢀⣠⣼⣿⣿⡏⠀⢠⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡀⠀⠀
          ⠀⠀⠀⣰⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀
          ⠀⠀⢰⣿⣿⡿⣿⣿⣿⡇⠀⠘⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⣿⠁⠀⠀
          ⠀⠀⣿⣿⣿⠁⣿⣿⣿⡇⠀⠀⠻⣿⣿⣿⣷⣶⣶⣶⣶⣶⣿⣿⣿⣿⠃⠀⠀⠀
          ⠀⢰⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
          ⠀⢸⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⢉⣿⣿⠀⠀⠀⠀⠀⠀
          ⠀⢸⣿⣿⣇⠀⣿⣿⣿⠀⠀⠀⠀⠀⢀⣤⣤⣤⡀⠀⠀⢸⣿⣿⣿⣷⣦⠀⠀⠀
          ⠀⠀⢻⣿⣿⣶⣿⣿⣿⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣦⡀⠀⠉⠉⠻⣿⣿⡇⠀⠀
          ⠀⠀⠀⠛⠿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠈⠹⣿⣿⣇⣀⠀⣠⣾⣿⣿⡇⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣦⣤⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⠿⠋⠉⠛⠋⠉⠉⠁⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁

"""


class ServerCore:
    db = USER_DATABASE

    def __init__(self, ip=FIXED_SERVER_IP, port=FIXED_SERVER_PORT, ):
        self.__should_close = False
        self._ip = ip
        self._port = port
        self._desc = (self.ip, self.port)

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def desc(self):
        return self._desc

    @ip.setter
    def ip(self, new_ip):
        self._ip = new_ip
        self._desc = (new_ip, self.port)

    @port.setter
    def port(self, new_port):
        self._port = new_port
        self._desc = (self.ip, new_port)

    @desc.setter
    def desc(self, new_desc):
        self._desc = new_desc
        self._ip, self._port = new_desc

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
            client_s.bind((self.ip, self.port + 1))

            # Receive the client connection
            client_s.listen()
            LOGGER.info("Waiting for client connection")
            client_conn, client_addr = client_s.accept()
            LOGGER.info(f"Connection with client {client_conn} accepted")

            while not self.__should_close:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as user_recv_s:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as user_s:
                            user_recv_s.bind(self.desc)

                            # Receive the initial user connection
                            user_recv_s.listen()
                            LOGGER.info(f"Waiting for a user connection, socket {user_recv_s}")
                            conn, addr = user_recv_s.accept()
                            LOGGER.info(f"Connection with {conn} accepted")

                            # Redirect the connection to another port
                            port = PortAssigner.get_port()
                            user_s.bind((self.ip, port))
                            user_s.listen()
                            conn.send(f"@redirect_port {port}".encode())

                            # Accept the connection to the new port
                            conn, addr = user_s.accept()
                            LOGGER.info(f"Assigned {addr} to port {port}")
                            conn.send(WELCOME_MSG.encode())

                            user_thread = threading.Thread(target=handle_user, args=(self.db, conn, user_s, client_s, port))
                            user_thread.start()

                except:
                    LOGGER.warning("Closing server.")
                    self.close()

                finally:
                    self.clean_up()

    def close(self):
        self.__should_close = True

    def clean_up(self):
        pass
