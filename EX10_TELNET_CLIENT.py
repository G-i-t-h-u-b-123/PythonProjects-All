import socket
def start_client(host='127.0.0.1', port=25):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    while True:
        response = client.recv(4096).decode() # Receive data from the server
        print(response, end='') # Print server response
        if "Goodbye!" in response or "Login failed" in response:
            break
        command = input() # Get user input
        client.send(command.encode()) # Send command to the server
    client.close()
if __name__ == "__main__":
    start_client()