from cam_common.configs import PORTS_FOR_USERS
from cam_common.logger import LOGGER


class PortAssigner:
    __free_ports = PORTS_FOR_USERS.copy()
    __used_ports = []
    __port_mapping = {}

    @staticmethod
    def get_port():
        try:
            port = PortAssigner.__free_ports.pop()
            PortAssigner.__used_ports.append(port)
            LOGGER.info(
                f"Got port {port}, free ports {PortAssigner.__free_ports}, used ports {PortAssigner.__used_ports}"
            )
            return port
        except IndexError:
            return -1

    @staticmethod
    def release_port(port):
        try:
            idx = PortAssigner.__used_ports.index(port)
            PortAssigner.__free_ports.append(PortAssigner.__used_ports.pop(idx))
            del PortAssigner.__port_mapping[port]
            LOGGER.info(
                f"Released port {port}, free ports {PortAssigner.__free_ports}, used ports {PortAssigner.__used_ports}"
            )
            return True
        except ValueError:
            return False

    @staticmethod
    def get_port_mapping():
        return PortAssigner.__port_mapping

    @staticmethod
    def assign_user_to_port(port, user):
        PortAssigner.__port_mapping[port] = user

    @staticmethod
    def get_sock_from_port(port):
        return PortAssigner.__port_mapping[port]

    @staticmethod
    def get_port_from_addr(addr):
        socket_mapping = {val[1]: key for key, val in PortAssigner.__port_mapping.items()}
        return socket_mapping[addr]

    def __enter__(self):
        self.__port = PortAssigner.get_port()
        return self.__port

    def __exit__(self, *_, **__):
        PortAssigner.release_port(self.__port)


class UserIdentifier:
    def __init__(self, username, socket, address):
        self.username = username
        self.socket = socket
        self.address = address



def format_port_mapping(port_mapping):
    result = "+------------+-----------------+-----------------+\n"
    result += "| Port       | Username        | Address         |\n"
    result += "+------------+-----------------+-----------------+\n"
    for port, user in port_mapping.items():
        result += f"| {str(port):10} | {user.username:15} | {user.address[0]:15} |\n"
    result += "+------------+-----------------+-----------------+\n"
    return result
