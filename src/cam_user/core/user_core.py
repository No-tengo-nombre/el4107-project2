import socket

from cam_common.configs import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, DEFAULT_TIMEOUT
from cam_common.logger import LOGGER
from cam_common.utils import receive_full_msg, EMPTY_SOCKET
from cam_user.core.packet_handle import handle_packet, handle_auth, handle_reconnection


class UserCore:
    def __init__(self, ip=DEFAULT_SERVER_IP, port=DEFAULT_SERVER_PORT, timeout=DEFAULT_TIMEOUT):
        self.__should_close = False
        self._ip = ip
        self._port = port
        self._desc = (self.ip, self.port)
        self._timeout = timeout
        self.__initial_socket = EMPTY_SOCKET
        self.__reconn_socket = EMPTY_SOCKET

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

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

    @desc.setter
    def desc(self, new_desc):
        self._desc = new_desc
        self._ip, self._port = new_desc

    @timeout.setter
    def timeout(self, new_timeout):
        self._timeout = new_timeout
        self.__server_socket.settimeout(new_timeout)
        self.__target_socket.settimeout(new_timeout)

    def close(self):
        self.__should_close = True

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initial_s:
            self.__initial_socket = initial_s
            initial_s.settimeout(self.timeout)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reconn_s:
                self.__reconn_socket = reconn_s
                reconn_s.settimeout(self.timeout)

                # Accept the connection and redirect the port
                LOGGER.info("Connecting to the initial socket")
                initial_s.connect(self.desc)
                LOGGER.info("Redirecting connection")
                handle_reconnection(self, initial_s, reconn_s, self.ip)
                LOGGER.info("Redirected connection")

                # Receive the welcome message
                # welcome_msg = reconn_s.recv(RECEIVING_WINDOW)
                welcome_msg = receive_full_msg(reconn_s)
                print(welcome_msg.decode())

                # Authenticate and receive stuff
                LOGGER.info("Authenticating")
                handle_auth(self, reconn_s)

                LOGGER.info("Finished authentication, going to main information flow")
                while not self.__should_close:
                    # packet = reconn_s.recv(RECEIVING_WINDOW)
                    packet = receive_full_msg(reconn_s)
                    handle_packet(self, packet.decode(), reconn_s)
