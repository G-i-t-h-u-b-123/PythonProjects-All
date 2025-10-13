import socket

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    print(f"Received: {message}")

                    if message.lower() == "ping":
                        response = "pong"
                    elif message.lower().startswith("echo "):
                        response = message[5:]  # Echo back the message after "echo "
                    elif message.lower().startswith("talk "):
                        response = f"Talk response: {message[5:]}"
                    else:
                        response = "Unknown command"

                    conn.sendall(response.encode())  # Send the response back

if __name__ == "__main__":
    start_server()
