from cam_common.configs import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT


class ClientCore:
    def __init__(self, server_ip=DEFAULT_SERVER_IP, server_port=DEFAULT_SERVER_PORT) -> None:
        self.__should_close = False
        self._server_ip = server_ip
        self._server_port = server_port
        self._server_desc = (server_ip, server_port)

    @property
    def server_ip(self):
        return self._server_ip

    @property
    def server_port(self):
        return self._server_port

    @property
    def server_desc(self):
        return self._server_desc

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
