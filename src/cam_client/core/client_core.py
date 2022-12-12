from cam_common.configs import (
    DEFAULT_SERVER_IP,
    DEFAULT_CLIENT_PORT,
    LOCAL_CAMERA_IP,
    LOCAL_CAMERA_PORT,
)
from cam_common.logger import LOGGER
from cam_client.core.proxy_handle import handle_information_flow

import socket


class ClientCore:
    def __init__(
        self,
        server_ip=DEFAULT_SERVER_IP,
        server_port=DEFAULT_CLIENT_PORT,
        target_ip=LOCAL_CAMERA_IP,
        target_port=LOCAL_CAMERA_PORT,
    ) -> None:
        self.__should_close = False
        self._server_ip = server_ip
        self._server_port = server_port
        self._server_desc = (server_ip, server_port)
        self._target_ip = target_ip
        self._target_port = target_port
        self._target_desc = (target_ip, target_port)

    @property
    def server_ip(self):
        return self._server_ip

    @property
    def server_port(self):
        return self._server_port

    @property
    def server_desc(self):
        return self._server_desc

    @property
    def target_ip(self):
        return self._target_ip

    @property
    def target_port(self):
        return self._target_port

    @property
    def target_desc(self):
        return self._target_desc

    @server_ip.setter
    def server_ip(self, new_ip):
        self._server_ip = new_ip
        self._server_desc = (new_ip, self.server_port)

    @server_port.setter
    def server_port(self, new_port):
        self._server_port = new_port
        self._server_desc = (self.ip, new_port)

    @server_desc.setter
    def server_desc(self, new_server_desc):
        self._server_desc = new_server_desc
        self._server_ip, self._server_port = new_server_desc

    @target_ip.setter
    def target_ip(self, new_ip):
        self._target_ip = new_ip
        self._target_desc = (new_ip, self.target_port)

    @target_port.setter
    def target_port(self, new_port):
        self._target_port = new_port
        self._target_desc = (self.ip, new_port)

    @target_desc.setter
    def target_desc(self, new_target_desc):
        self._target_desc = new_target_desc
        self._target_ip, self._target_port = new_target_desc

    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_s:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_s:
                    # Connect to the server and target
                    LOGGER.info("Connecting to server")
                    server_s.connect(self.server_desc)
                    LOGGER.info("Connecting to target")
                    target_s.connect(self.target_desc)

                    LOGGER.info("Initializing proxy")
                    while not self.__should_close:
                        handle_information_flow(server_s, target_s)
                    LOGGER.info("Finished connection")

        except Exception as e:
            LOGGER.critical(f"Closing client, found exception {e}")
            self.close()

        finally:
            self.clean_up()

    def close(self):
        self.__should_close = True

    def clean_up(self):
        pass
