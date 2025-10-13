import socket
import os

# Receiver details (Replace with receiver's IP)
server_ip = "127.0.0.1"  # Example receiver IP
server_port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

filename = input("Enter the filename to send: ")

if not os.path.exists(filename):
    print("File not found!")
    s.close()
    exit()

# Send filename first
s.sendto(filename.encode(), (server_ip, server_port))

# Send file content
with open(filename, 'rb') as f:
    while True:
        bytes_read = f.read(4096)
        if not bytes_read:
            break
        s.sendto(bytes_read, (server_ip, server_port))

# Send end signal
s.sendto(b'END', (server_ip, server_port))
print("File sent successfully.")

s.close()
