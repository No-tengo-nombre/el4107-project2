from camcommon import RECEIVING_WINDOW, END_AUTH_SUCCESS_STRING, END_AUTH_FAILURE_STRING


def handle_auth(sv_socket):
    while True:
        packet = sv_socket.recv(RECEIVING_WINDOW)
        if packet.decode() == END_AUTH_SUCCESS_STRING:
            break
        elif packet.decode() == END_AUTH_FAILURE_STRING:
            packet = sv_socket.recv(RECEIVING_WINDOW)
            print(packet.decode())
            break

        print(packet.decode())
        print(">>> ", end="")
        sv_socket.send(input().encode())


def handle_packet(packet, client):
    client.close()
