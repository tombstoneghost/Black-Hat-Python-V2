# Imports
import socket

print("#"*5 + "UDP CLIENT" + "#"*5)

target_host = input("[?] Enter Target Host: ") # google.com
target_port = int(input("[?] Enter Target Port: ")) # 80

print("[!] Establishing Connection")

# Socket Object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("[!] Sending Data")

# Send Data
client.sendto(b"aabbccddeeff", (target_host, target_port))

print("[!] Data Received")

# Receive Data
resp, addr = client.recvfrom(4096)

print(resp.decode())

# Connection Closed
client.close()

print("[!] Connection Closed")

