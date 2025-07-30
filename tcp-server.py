import socket
import os

def receive_file(conn, filename):
    with open(filename, 'w') as f:
        while True:
            data = conn.recv(1024).decode()
            if data == "END":  # End of file transfer
                print(f"Finished receiving {filename}")
                break
            f.write(data)
            print(f"Receiving... {len(data)} bytes")
    f.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    with conn:
        while True:
            # Wait for a command from the client
            command = conn.recv(1024).decode()
            if not command:
                break
            print(f"Command received: {command}")

            if command.startswith("UPLOAD"):
                # Command format: "UPLOAD filename"
                _, filename = command.split()
                print(f"Receiving file: {filename}")
                receive_file(conn, filename)

            elif command == "LIST":
                # Send the list of files in the current directory
                files = os.listdir()
                conn.send("\n".join(files).encode())
            
            elif command == "QUIT":
                print("Client disconnected.")
                break

    server_socket.close()
