from cam_common.configs import PORTS_FOR_USERS
from cam_common.logger import LOGGER


class PortAssigner:
    __free_ports = PORTS_FOR_USERS.copy()
    __used_ports = []

    @staticmethod
    def get_port():
        try:
            port = PortAssigner.__free_ports.pop()
            PortAssigner.__used_ports.append(port)
            LOGGER.info(f"Got port {port}, free ports {PortAssigner.__free_ports}, used ports {PortAssigner.__used_ports}")
            return port
        except IndexError:
            return -1

    @staticmethod
    def release_port(port):
        try:
            idx = PortAssigner.__used_ports.index(port)
            PortAssigner.__free_ports.append(PortAssigner.__used_ports.pop(idx))
            LOGGER.info(f"Released port {port}, free ports {PortAssigner.__free_ports}, used ports {PortAssigner.__used_ports}")
            return True
        except ValueError:
            return False

    def __enter__(self):
        self.__port = PortAssigner.get_port()
        return self.__port

    def __exit__(self, *_, **__):
        PortAssigner.release_port(self.__port)
