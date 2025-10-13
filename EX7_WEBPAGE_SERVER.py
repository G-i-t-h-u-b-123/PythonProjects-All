import socket
import os

def handle_request(conn):
    request = conn.recv(1024).decode()
    headers = request.splitlines()
    method = headers[0].split()[0]
    filename = headers[0].split()[1][1:]  # Get the filename from the request

    if method == 'GET':
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                response_body = f.read()
            response_header = 'HTTP/1.1 200 OK\n\n'
            conn.sendall(response_header.encode() + response_body)
        else:
            # Create the file if it does not exist
            with open(filename, 'wb') as f:
                f.write(b'')  # Create an empty file
            response_header = 'HTTP/1.1 201 CREATED\n\nFile created: ' + filename
            conn.sendall(response_header.encode())

    elif method == 'PUT':
        # Save the uploaded file
        body = request.split('\n\n')[1]
        with open(filename, 'wb') as f:
            f.write(body.encode())
        response_header = 'HTTP/1.1 201 CREATED\n\n'
        conn.sendall(response_header.encode())

    conn.close()

def start_server(port=8081):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    print(f'Server listening on port {port}')

    while True:
        conn, addr = server_socket.accept()
        print(f'Connection from {addr}')
        handle_request(conn)

if __name__ == "__main__":
    start_server()