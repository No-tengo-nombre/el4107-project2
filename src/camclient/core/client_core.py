import socket

from camcommon import FIXED_SERVER_DESC, FIXED_SERVER_IP, RECEIVING_WINDOW
from camclient.core.packet_handle import handle_packet, handle_auth, handle_reconnection


class ClientCore:
    def __init__(self):
        self.__should_close = False

    def close(self):
        self.__should_close = True

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
                # Accept the connection and redirect the port
                s.connect(FIXED_SERVER_DESC)
                handle_reconnection(s, client_s)

                # Receive the welcome message
                welcome_msg = client_s.recv(RECEIVING_WINDOW)
                print(welcome_msg.decode())

                # Authenticate and receive stuff
                handle_auth(client_s)
                while not self.__should_close:
                    packet = client_s.recv(RECEIVING_WINDOW)
                    handle_packet(packet, self)
