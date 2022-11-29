import socket
import threading

from camcommon import FIXED_CAMERA_DESC, FIXED_SERVER_PORT
from camcommon.logger import LOGGER
from camserver.core.user_handle import handle_user


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
    def __init__(self):
        self.__should_close = False

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as camera_s:
                s.bind(("", FIXED_SERVER_PORT))
                camera_s.bind(FIXED_CAMERA_DESC)
                s.listen()

                while not self.__should_close:
                    conn, addr = s.accept()
                    LOGGER.info(f"Connection accepted from address {addr}")
                    conn.send(WELCOME_MSG.encode())

                    user_thread = threading.Thread(target=handle_user, args=(conn, s, camera_s))
                    user_thread.start()
