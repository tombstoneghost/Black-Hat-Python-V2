import sys
import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


# Dump data in Hex format
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3

        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

        if show:
            for line in results:
                print(line)
            else:
                return results


# Receive Data from the Proxy
def receive_from(connection):
    buffer = b""

    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break

            buffer = buffer + data
    except Exception as e:
        pass

    return buffer


# Request Handler
def request_handler(buffer):
    # Packet Modifications
    return buffer


# Response Handler
def response_handler(buffer):
    # Packet Modifications
    return buffer


# Handle Proxy
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
    
    remote_buffer = response_handler(remote_buffer)

    if len(remote_buffer):
        print(f"[<==] Sending {len(remote_buffer)} bytes to localhost.")
        client_socket.send(remote_buffer)
    
    while True:
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            line = f"[==>] Received {len(local_buffer)} from localhost"
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote")

        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print(f"[<==] Received {len(remote_buffer)} from remote.")
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[!] No more data. Closing connections")
            break


# Server Loop
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("Problem on bind:", e)
        print(f"[!] Failed to listen on {local_host}:{local_port}")
        print("[!] Check for other listeners or correct permissions")
        sys.exit(0)
    
    print(f"[!] Listening on {local_host}:{local_port}")
    server.listen()

    while True:
        client_socket, addr = server.accept()

        line = f"> Recieved incoming information from {addr[0]}:{addr[1]}"
        print(line)

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


# Main Function
def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first.capitalize():
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host=local_host, local_port=local_port, remote_host=remote_host, remote_port=remote_port, receive_first=receive_first)



if __name__ == "__main__":
    main()
