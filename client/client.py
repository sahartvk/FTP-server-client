import socket
import sys


server_ip = '127.0.0.1'
server_port = 1234

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting...")
clientSocket.connect((server_ip, server_port))
print("connected to server successfully")


def help():
    clientSocket.send("help".encode())
    help_size = int(clientSocket.recv(1024).decode())
    help = clientSocket.recv(help_size).decode()
    print(help)
    return


def pwd():
    clientSocket.send("pwd".encode())
    pwd_size = int(clientSocket.recv(1024).decode())
    pwd = clientSocket.recv(pwd_size).decode()
    print(pwd)
    return


def list():
    clientSocket.send("list".encode())
    clientSocket.recv(1024)

    size_ = int(clientSocket.recv(1024).decode())
    list_ = clientSocket.recv(size_).decode()
    total_size = clientSocket.recv(1024).decode()

    print(list_)
    print(f"total size :   {total_size}\n")
    return


def cd(directory_name: str):
    clientSocket.send("cd".encode())
    clientSocket.recv(1024)

    clientSocket.send(directory_name.encode())

    status = clientSocket.recv(1024).decode()
    if status == "invalid":
        print("invalid directory")
    elif status == "changed":
        print(f"changed to {directory_name}")


def dwld(file_name: str):
    clientSocket.send("dwld".encode())
    clientSocket.recv(1024)

    # 1
    clientSocket.send(str(sys.getsizeof(file_name)).encode())
    clientSocket.send(file_name.encode())

    # 2
    file_size = int(clientSocket.recv(1024).decode())
    if file_size == -1:
        print("there is no file with that name!")
        return

    clientSocket.send("ok".encode())

    # 3
    new_port = int(clientSocket.recv(1024).decode())
    dwld_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dwld_sock.connect((server_ip, new_port))
    # connected to new port successfully

    # 4
    print("downloading...")
    output_file = open(file_name, "wb")
    file = dwld_sock.recv(file_size)
    output_file.write(file)
    print("downloaded successfully")
    dwld_sock.send("ok".encode())
    output_file.close()

    # 5
    dwld_sock.send("completed".encode())
    dwld_sock.recv(1024)
    dwld_sock.send("ok".encode())
    dwld_sock.close()
    # download socket closed

    return


# print help
help()

while True:

    command = input("$ ")
    command.lower()

    if command == "help":
        help()
    elif command == "list":
        list()
    elif command == "pwd":
        pwd()
    elif command[0:2] == "cd":
        if command[3:]:
            cd(command[3:])
    elif command[0:4] == "dwld":
        if command[5:]:
            dwld(command[5:])
    elif command == "quit":
        print("exiting...")
        clientSocket.send("quit".encode())
        clientSocket.close()
        break
    else:
        print("invalid command")
        clientSocket.send("invalid command".encode())
