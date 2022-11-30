from camcommon import RECEIVING_WINDOW, END_AUTH_STRING


def handle_auth(sv_socket):
    while True:
        packet = sv_socket.recv(RECEIVING_WINDOW)
        if packet.decode() == END_AUTH_STRING:
            break
        print(packet.decode(), end="")
        sv_socket.send(input().encode())


def handle_packet(packet):
    print(packet)
    print(packet.decode())
