from cam_common.configs import RECEIVING_WINDOW
from cam_common.logger import LOGGER
from cam_common.utils import receive_full_msg, send_full_msg


def handle_information_flow(server_socket, target_socket):
    # Act as a proxy
    LOGGER.debug("Listening for server packet")
    packet = receive_full_msg(server_socket)
    LOGGER.debug("Sending packet to target")
    # send_full_msg(target_socket, packet)
    target_socket.send(packet)
    LOGGER.debug("Listening for target packet")
    # response = receive_full_msg(target_socket)
    response = target_socket.recv(RECEIVING_WINDOW)
    LOGGER.debug("Sending packet to server")
    send_full_msg(server_socket, response)
