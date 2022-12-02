from cam_common.configs import RECEIVING_WINDOW
from cam_common.logger import LOGGER


def handle_information_flow(server_socket, target_socket):
    # Act as a proxy
    LOGGER.debug("Listening for server packet")
    packet = server_socket.recv(RECEIVING_WINDOW)
    LOGGER.debug("Sending packet to target")
    target_socket.send(packet)
    LOGGER.debug("Listening for target packet")
    response = target_socket.recv(RECEIVING_WINDOW)
    LOGGER.debug("Sending packet to server")
    server_socket.send(response)
