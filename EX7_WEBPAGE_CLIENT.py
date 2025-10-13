import socket
import os


def upload_file(filename, server_ip, port=8081):
    try:
        # Open the file in binary read mode
        with open(filename, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        return

    # Construct the HTTP PUT request
    request = f'PUT /{filename} HTTP/1.1\nHost: {server_ip}\nContent-Length: {len(file_data)}\n\n'
    request = request.encode() + file_data

    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Send the request to the server
    client_socket.sendall(request)

    # Receive the server's response
    response = client_socket.recv(4096).decode()
    print('Response from server:', response)

    # Check if the file was created or overwritten
    if '201 CREATED' in response:
        print(f'Uploaded {filename} successfully (file created).')
    elif '200 OK' in response:
        print(f'Uploaded {filename} successfully (file overwritten).')
    else:
        print('Failed to upload the file.')

    # Close the socket
    client_socket.close()


def download_file(filename, server_ip, port=8081):
    # Construct the HTTP GET request
    request = f'GET /{filename} HTTP/1.1\nHost: {server_ip}\n\n'.encode()

    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Send the request to the server
    client_socket.sendall(request)

    # Receive the server's response
    response = client_socket.recv(4096).decode()
    headers, body = response.split('\n\n', 1)

    # Check the response headers
    if '200 OK' in headers:
        with open(filename, 'wb') as f:
            f.write(body.encode())
        print(f'Downloaded {filename} successfully.')
        print(body)  # Display the content of the file
    else:
        print('File not found on server.')

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    server_ip = '127.0.0.1'  # Change to your server's IP if needed
    # Uncomment to upload
    #upload_file('ss1.html', server_ip)

    # Uncomment to download
    download_file('ss1.html', server_ip)
