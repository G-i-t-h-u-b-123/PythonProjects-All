import socket
import os
import platform

def open_image(file_path):
    # Open the image using the default image viewer
    if platform.system() == 'Windows':
        os.startfile(file_path)  # Windows
    elif platform.system() == 'Darwin':  # macOS
        os.system(f'open "{file_path}"')
    else:  # Linux
        os.system(f'xdg-open "{file_path}"')

def request_capture(host='127.0.0.1', port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    # Send capture request
    client.sendall('CAPTURE'.encode('utf-8'))
    # Receive image data length
    image_length = int.from_bytes(client.recv(4), 'big')
    # Receive the actual image data
    image_data = b''
    while len(image_data) < image_length:
        packet = client.recv(4096)
        if not packet:
            break
        image_data += packet
    # Save the image
    file_path = 'screenshot.png'
    with open(file_path, 'wb') as f:
        f.write(image_data)
    print("Screenshot saved as 'screenshot.png'")
    # Open the image
    open_image(file_path)
    # Optionally, send a quit signal
    client.sendall('QUIT'.encode('utf-8'))
    client.close()

if __name__ == '__main__':
    request_capture()
