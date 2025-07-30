import socket
import os

def send_file(sock, filename):
    try:
        with open(filename, 'r') as fi:
            data = fi.read(1024)
            while data:
                sock.send(data.encode())
                data = fi.read(1024)
            sock.send("END".encode())  # Signal end of file
        print("File sent successfully.")
    except IOError:
        print("Invalid filename or file not found.")

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print("Unable to connect to the server. Make sure the server is running.")
        exit()

    while True:
        # Show command options to the user
        command = input("Enter command (UPLOAD <filename>, LIST, QUIT): ").strip()

        if command.upper().startswith("UPLOAD"):
            _, filename = command.split()
            sock.send(command.encode())  # Send "UPLOAD filename" command
            send_file(sock, filename)

        elif command.upper() == "LIST":
            sock.send("LIST".encode())  # Send "LIST" command
            files = sock.recv(4096).decode()
            print("Files on server:\n" + files)

        elif command.upper() == "QUIT":
            sock.send("QUIT".encode())  # Send "QUIT" command
            print("Disconnected from server.")
            break

        else:
            print("Invalid command. Try again.")

    sock.close()
