from camcommon import RECEIVING_WINDOW, END_AUTH_SUCCESS_STRING, END_AUTH_FAILURE_STRING
from getpass import getpass


def handle_auth(sv_socket):
    while True:
        packet = sv_socket.recv(RECEIVING_WINDOW)
        if packet.decode() == END_AUTH_SUCCESS_STRING:
            print("Successfuly validated user :)")
            break
        elif packet.decode() == END_AUTH_FAILURE_STRING:
            print("Failed to validate user :(")
            break

        handle_command(packet.decode(), server_socket=sv_socket)


def handle_command(cmd, server_socket):
    action, *args = cmd.split(" ")
    if action[0] == "@":
        globals()[f"__token_action_{action[1:]}"](args, server_socket=server_socket)


def handle_packet(packet, client):
    client.close()


# Available commands
# ==================
# echo ARGS         -> Print to the user's console.
# input ARGS        -> Print ARGS and get user input.
# hidden_input ARGS -> Print ARGS and get user input,
#                      without showing input to console.


def __token_action_echo(args, server_socket):
    print(*args)


def __token_action_input(args, server_socket):
    print(*args)
    print(">>> ", end="")
    server_socket.send(input().encode())


def __token_action_hidden_input(args, server_socket):
    print(*args)
    server_socket.send(getpass(">>> ").encode())
