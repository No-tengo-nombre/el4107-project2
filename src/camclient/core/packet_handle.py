from camcommon import RECEIVING_WINDOW, FIXED_SERVER_IP
from camcommon.signals import SIGNAL_BREAK
from getpass import getpass


def handle_reconnection(sv_socket, client_socket):
    packet = sv_socket.recv(RECEIVING_WINDOW)
    signal = handle_command(packet.decode(), server_socket=sv_socket, client_socket=client_socket)


def handle_auth(sv_socket):
    while True:
        packet = sv_socket.recv(RECEIVING_WINDOW)
        signal = handle_command(packet.decode(), server_socket=sv_socket)
        if signal == SIGNAL_BREAK:
            break


def handle_command(cmd, *handle_args, **handle_kwargs):
    action, *args = cmd.split(" ")
    if action[0] == "@":
        globals()[f"__server_action_{action[1:]}"](args, *handle_args, **handle_kwargs)


def handle_packet(packet, client):
    client.close()


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


def __server_action_echo(args, **_):
    print(*args)


def __server_action_input(args, server_socket, **__):
    print(*args)
    print(">>> ", end="")
    server_socket.send(input().encode())


def __server_action_hidden_input(args, server_socket, **__):
    print(*args)
    server_socket.send(getpass(">>> ").encode())


def __server_action_kick(args, server_socket, **__):
    print(*args)
    server_socket.close()
    quit()


def __server_action_break_while_loop(*_, **__):
    return SIGNAL_BREAK


def __server_action_redirect_port(args, server_socket, client_socket, **__):
    port = int(args[0])
    server_socket.close()
    client_socket.connect((FIXED_SERVER_IP, port))
