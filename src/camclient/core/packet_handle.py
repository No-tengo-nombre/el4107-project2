from camcommon import RECEIVING_WINDOW



def handle_auth(sv_socket):
    username_prompt = sv_socket.recv(RECEIVING_WINDOW)
    sv_socket.send(input(username_prompt.decode()).encode())
    pass_prompt = sv_socket.recv(RECEIVING_WINDOW)
    sv_socket.send(input(pass_prompt.decode()).encode())


def handle_packet(packet):
    print(packet)
    print(packet.decode())
