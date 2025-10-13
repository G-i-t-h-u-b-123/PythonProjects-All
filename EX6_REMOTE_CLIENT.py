import socket

def main():
    host = '127.0.0.1'  # Replace with the server's IP address
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        command = input("Enter command to execute (or 'exit' to quit): ")
        client_socket.send(command.encode())

        if command.lower() == 'exit':
            break

        # Receive the output from the server
        output = client_socket.recv(4096).decode()
        print(output)

    client_socket.close()

if __name__ == "__main__":
    main()
