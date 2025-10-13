import socket
import threading
import pyautogui
import io
from PIL import Image

def handle_client(client_socket):
    while True:
        # Wait for a request from the client
        request = client_socket.recv(1024).decode('utf-8')
        if request == 'CAPTURE':
            # Capture the screen
            screenshot = pyautogui.screenshot()
            byte_io = io.BytesIO()
            screenshot.save(byte_io, format='PNG')
            byte_io.seek(0)
            image_data = byte_io.getvalue()
            # Send image data length first
            client_socket.sendall(len(image_data).to_bytes(4, 'big'))
            # Then send the actual image data
            client_socket.sendall(image_data)
        elif request == 'QUIT':
            break

    client_socket.close()

def start_server(host='127.0.0.1', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()
