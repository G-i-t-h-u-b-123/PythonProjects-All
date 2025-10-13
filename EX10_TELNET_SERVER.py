import socket
import threading
import subprocess
#Sample user credentials (username : password)
USER_CREDENTIALS = { "user" : "password123","admin" : "adminpass"}
def handle_client(client_socket):
    client_socket.send(b"Welcome to the TELNET server!\n")
    client_socket.send(b"Please enter your username: ")
    username = client_socket.recv(1024).decode().strip()
    client_socket.send(b"Please enter your password: ")
    password = client_socket.recv(1024).decode().strip()
    # Authenticate user
    # if username in USER_CREDENTIALS and USER_CREDENTIALS[username] ==password:
    client_socket.send(b"Login successful!\n")
    client_socket.send(b"Type your command (or 'exit' to disconnect): \n")
    while True:
        client_socket.send(b">")  # Prompt for command
        command = client_socket.recv(1024).decode().strip()

        if command.lower() == 'exit':
            client_socket.send(b"Goodbye!\n")
            break
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            client_socket.send(output + b"\n")  # Send output back to client
        except subprocess.CalledProcessError as e:
            client_socket.send(e.output + b"\n")  # Send error output back to client

        else:
            client_socket.send(b"Login failed. Disconnecting...\n")
        client_socket.close()

def start_server(host = '127.0.0.1', port = 25):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[*]Listening on {host} : {port} ")
    while True:
        client_socket, addr = server.accept()
        print(f"[*]Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()