import socket

HOST = '127.0.0.1'
PORT = 6001


def file_client():
    filename = input("Enter the file name to send: ")

    try:
        with open(filename, 'rb') as f:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                # Send filename followed by newline to let server know where filename ends
                s.sendall((filename + '\n').encode())
                print("[File Client] Sending file...")

                # Send file content
                while chunk := f.read(1024):
                    s.sendall(chunk)

                print(f"[File Client] File '{filename}' sent successfully.")
    except FileNotFoundError:
        print(f"[File Client] Error: File '{filename}' not found.")


if __name__ == "__main__":
    file_client()