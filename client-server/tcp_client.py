# Imports
import socket

print("#"*5 + "TCP CLIENT" + "#"*5)

target_host = input("[?] Enter Target Host: ") # google.com
target_port = int(input("[?] Enter Target Port: ")) # 80

print("[!] Establishing Connection")

# Socket Object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the Client
client.connect((target_host, target_port))

print("[+] Connection Established")

print("[!] Sending Data")

# Send Data
client.send(b"GET / HTTP/1.1\r\Host: google.com\r\n\r\n")

print("[!] Data Received")

# Receive Data
resp = client.recv(4096)

print(resp.decode())

# Connection Closed
client.close()

print("[!] Connection Closed")

