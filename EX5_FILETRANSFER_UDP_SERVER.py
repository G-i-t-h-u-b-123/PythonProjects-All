import socket

# Server details
server_ip = "127.0.0.1"      # Listen on all interfaces
server_port = 9999

# Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((server_ip, server_port))

print(f"UDP Server started on port {server_port}. Waiting for file...")

# Receive file name
data, addr = s.recvfrom(1024)
filename = data.decode()
print(f"Receiving file: {filename} from {addr}")

# Open file for writing
with open(filename, 'wb') as f:
    while True:
        data, addr = s.recvfrom(4096)
        if data == b'END':
            break
        f.write(data)

print("File received successfully.")
s.close()
