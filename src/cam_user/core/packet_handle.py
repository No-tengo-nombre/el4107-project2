from cam_common.configs import RECEIVING_WINDOW
from cam_common.logger import LOGGER
from cam_common.signals import SIGNAL_BREAK
from cam_common.utils import receive_full_msg, send_full_msg
from getpass import getpass

import webbrowser


def handle_reconnection(user, sv_socket, reconnection_socket, server_ip):
    # packet = sv_socket.recv(RECEIVING_WINDOW)
    packet = receive_full_msg(sv_socket)
    LOGGER.debug("Received reconnection packet")
    signal = handle_command(
        user,
        packet.decode(),
        server_socket=sv_socket,
        reconnection_socket=reconnection_socket,
        server_ip=server_ip,
    )


def handle_auth(user, sv_socket):
    while True:
        # packet = sv_socket.recv(RECEIVING_WINDOW)
        packet = receive_full_msg(sv_socket)
        LOGGER.debug("Received authentication packet")
        signal = handle_command(user, packet.decode(), server_socket=sv_socket)
        if signal is not None:
            LOGGER.debug(f"Got signal {signal}")
        if signal == SIGNAL_BREAK:
            LOGGER.debug("Breaking authentication loop")
            # sv_socket.send("OK".encode())
            send_full_msg(sv_socket, "OK".encode())
            break


def handle_command(user, cmd, *handle_args, **handle_kwargs):
    LOGGER.debug("Handling server command")
    action, *args = cmd.split(" ")
    for i, a in enumerate(args):
        if a[0] == "$":
            args[i] = getattr(user, a[1:])
    
    if action[0] == "@":
        return globals()[f"__server_action_{action[1:]}"](args, *handle_args, **handle_kwargs)


def handle_packet(user, packet, server_socket):
    LOGGER.debug("Received packet")
    handle_command(user, packet, server_socket)


# Available commands
# ==================
# echo ARGS             -> Print to the user's console.
# input ARGS            -> Print ARGS and get user input.
# hidden_input ARGS     -> Print ARGS and get user input,
#                          without showing input to console.
# kick ARGS             -> Kick the user, showing ARGS as the
#                          reason.
# break_while_loop      -> Send a signal to break a while loop.
# redirect_port [PORT]  -> Redirect the port that the user is
#                          connected to.


def __server_action_echo(args, server_socket, *_, **__):
    print(*args)
    # server_socket.send("OK".encode())
    send_full_msg(server_socket, "OK".encode())


def __server_action_input(args, server_socket, *_, **__):
    print(*args)
    print(">>> ", end="")
    # server_socket.send(input().encode())
    send_full_msg(server_socket, input().encode())


def __server_action_hidden_input(args, server_socket, *_, **__):
    print(*args)
    # server_socket.send(getpass(">>> ").encode())
    send_full_msg(server_socket, getpass(">>> ").encode())


def __server_action_kick(args, server_socket, *_, **__):
    print(*args)
    server_socket.close()
    quit()


def __server_action_break_while_loop(*_, **__):
    return SIGNAL_BREAK


def __server_action_redirect_port(args, server_socket, reconnection_socket, server_ip, **__):
    port = int(args[0])
    LOGGER.debug(f"Redirecting connection to {server_ip}:{port}")
    # server_socket.send("OK".encode())
    send_full_msg(server_socket, "OK".encode())
    server_socket.close()
    reconnection_socket.connect((server_ip, port))


def __server_action_webbrowser_new_tab(args, server_socket, *_, **__):
    address = f"{''.join(args[:-1])}:{args[-1]}"
    LOGGER.info(f"Received connection request to {address}")
    # server_socket.send("OK".encode())
    send_full_msg(server_socket, "OK".encode())
    webbrowser.get().open_new_tab(address)
