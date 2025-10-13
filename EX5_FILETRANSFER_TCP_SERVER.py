import socket

HOST = '127.0.0.1'
PORT = 6001


def file_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[File Server] Listening on port", PORT)
        while True:
            conn, _ = s.accept()
            with conn:
                print("[File Server] Connected.")
                buffer = b''
                filename = ''

                # Step 1: Receive filename terminated with newline
                while True:
                    data = conn.recv(1)
                    if not data:
                        break
                    if data == b'\n':
                        filename = buffer.decode().strip()
                        break
                    buffer += data

                print(f"[File Server] Receiving file: {filename}")
                with open(f"received_{filename}", 'wb') as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print(f"[File Server] File '{filename}' received and saved.")


if __name__ == "__main__":
    file_server()
