# Imports
import socket
import threading

print("#"*5 + "TCP SERVER" + "#"*5)

server_host = input("[?] Enter Server Host: ") # 0.0.0.0
server_port = int(input("[?] Enter Server Port: ")) # 9988

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode('utf-8')}")
        sock.send(b'ACK')

def main():
    print("[!] Setting up Server")

    # Socket Object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_host, server_port))
    server.listen()

    print(f"[!] Server Listening on {server_host}:{server_port}")
    print("[!] Waiting for Clients")

    while True:
        client, addr = server.accept()

        print(f"[+] Connection Request Accepted from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


if __name__ == "__main__":
    main()

