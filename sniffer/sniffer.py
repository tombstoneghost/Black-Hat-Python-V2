# Imports 
import socket
import os


HOST = input("Enter Host IP: ")

def main():
    # Windows
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    # Linux
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    # Include IP Header
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socekt.RCVALL_ON)

    print(sniffer.recvfrom(65565))

    # If Windows, Turn off Promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.SIO_RCVALL_OFF)


if __name__ == "__main__":
    main()
