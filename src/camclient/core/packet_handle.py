from camcommon import RECEIVING_WINDOW
from camcommon.signals import SIGNAL_BREAK
from getpass import getpass


def handle_auth(sv_socket):
    while True:
        packet = sv_socket.recv(RECEIVING_WINDOW)
        signal = handle_command(packet.decode(), server_socket=sv_socket)
        if signal == SIGNAL_BREAK:
            break


def handle_command(cmd, server_socket):
    action, *args = cmd.split(" ")
    if action[0] == "@":
        globals()[f"__server_action_{action[1:]}"](args, server_socket=server_socket)


def handle_packet(packet, client):
    client.close()


# Available commands
# ==================
# echo ARGS         -> Print to the user's console.
# input ARGS        -> Print ARGS and get user input.
# hidden_input ARGS -> Print ARGS and get user input,
#                      without showing input to console.
# kick ARGS         -> Kick the user, showing ARGS as the
#                      reason.


def __server_action_echo(args, server_socket):
    print(*args)


def __server_action_input(args, server_socket):
    print(*args)
    print(">>> ", end="")
    server_socket.send(input().encode())


def __server_action_hidden_input(args, server_socket):
    print(*args)
    server_socket.send(getpass(">>> ").encode())


def __server_action_kick(args, server_socket):
    print(*args)
    server_socket.close()
    quit()


def __server_action_break_while_loop(args, server_socket):
    return SIGNAL_BREAK
