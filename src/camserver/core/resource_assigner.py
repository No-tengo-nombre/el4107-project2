from camcommon.logger import LOGGER


class PortAssigner:
    __ALL_PORTS = list(range(10032, 10040))
    __free_ports = __ALL_PORTS.copy()
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

