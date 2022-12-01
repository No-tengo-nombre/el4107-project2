import socket

from camcommon import FIXED_SERVER_DESC, FIXED_SERVER_IP, FIXED_SERVER_PORT, RECEIVING_WINDOW
from camclient.core.packet_handle import handle_packet, handle_auth, handle_reconnection


class ClientCore:
    def __init__(self, ip=FIXED_SERVER_IP, port=FIXED_SERVER_PORT):
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

    def close(self):
        self.__should_close = True

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
                # Accept the connection and redirect the port
                s.connect(self.desc)
                handle_reconnection(s, client_s)

                # Receive the welcome message
                welcome_msg = client_s.recv(RECEIVING_WINDOW)
                print(welcome_msg.decode())

                # Authenticate and receive stuff
                handle_auth(client_s)
                while not self.__should_close:
                    packet = client_s.recv(RECEIVING_WINDOW)
                    handle_packet(packet, self)
