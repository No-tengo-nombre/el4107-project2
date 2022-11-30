from camcommon import RECEIVING_WINDOW, END_AUTH_SUCCESS_STRING, END_AUTH_FAILURE_STRING


def handle_auth(sv_socket):
    while True:
        packet = sv_socket.recv(RECEIVING_WINDOW)
        if packet.decode() == END_AUTH_SUCCESS_STRING:
            print("Successfuly validated user :)")
            break
        elif packet.decode() == END_AUTH_FAILURE_STRING:
            print("Failed to validate user :(")
            break

        print(packet.decode())
        print(">>> ", end="")
        sv_socket.send(input().encode())


def handle_packet(packet, client):
    client.close()
