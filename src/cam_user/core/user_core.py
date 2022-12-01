import socket

from cam_common import FIXED_SERVER_DESC, FIXED_SERVER_IP, FIXED_SERVER_PORT, RECEIVING_WINDOW
from cam_common.logger import LOGGER
from cam_user.core.packet_handle import handle_packet, handle_auth, handle_reconnection


class UserCore:
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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initial_s:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reconn_s:
                # Accept the connection and redirect the port
                LOGGER.info("Connecting to the initial socket")
                initial_s.connect(self.desc)
                LOGGER.info("Redirecting connection")
                handle_reconnection(initial_s, reconn_s, self.ip)

                # Receive the welcome message
                welcome_msg = reconn_s.recv(RECEIVING_WINDOW)
                print(welcome_msg.decode())

                # Authenticate and receive stuff
                LOGGER.info("Authenticating")
                handle_auth(reconn_s)

                LOGGER.info("Finished authentication, going to main information flow")
                while not self.__should_close:
                    packet = reconn_s.recv(RECEIVING_WINDOW)
                    handle_packet(packet, self)
