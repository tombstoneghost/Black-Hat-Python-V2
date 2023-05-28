# Imports
import ipaddress
import os
import socket
import struct
import sys
import threading
import time


MESSAGE = "PYTHONRULES!"


# Class IP
class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dest = header[9]

        # Human Readable IP address
        self.src_address = ipaddress.ip_address(self.src)
        self.dest_address = ipaddress.ip_address(self.dest)

        # Protcol constants to name
        self.protocol_map = {
            1: 'ICMP',
            6: 'TCP',
            17: 'UDP'
        }

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print(f"{e} No Protocol for {self.protocol_num}")
            self.protocol = str(self.protocol_num)

# Class ICMP
class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

    
# Spray UDP Datagrams
def udp_sender(subnet):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(subnet).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))


# Clas Scanner:
class Scanner:
    def __init__(self, host, subnet):
        self.host = host
        self.subnet = subnet

        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.sock.bind((host, 0))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = set([f'{str(self.host)} *'])

        try:
            while True:
                raw_buffer = self.sock.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[:20])

                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buff = raw_buffer[offset:offset + 8]

                    icmp_header = ICMP(buff=buff)

                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(self.subnet):
                            if raw_buffer[len(raw_buffer) - len(MESSAGE)] == bytes(MESSAGE, 'utf-8'):
                                tgt = str(ip_header.src_address)

                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f'Host Up: {tgt}')

        except KeyboardInterrupt:
            if os.name == 'nt':
                sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            
            if hosts_up:
                print(f'\n\nSummary: Hosts up on {self.subnet}')

                for host in sorted(hosts_up):
                    print(f'{host}')
                print('')
            sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        host = sys.argv[1]
        subnet = sys.argv[2]

        s = Scanner(host=host, subnet=subnet)
        time.sleep(5)
        t = threading.Thread(target=udp_sender, args=(subnet,))
        t.start()
        s.sniff()
    else:
        print("Usage: sudo python3 scanner.py [HOST] [SUBNET]")
