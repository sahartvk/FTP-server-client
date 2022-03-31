import socket
import sys
import os
import random


server_ip = '127.0.0.1'
server_port = 1234

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((server_ip, server_port))
print("listening...")
serverSocket.listen(5)

sock, addr = serverSocket.accept()
print(f"client connected by address {addr}")


def help():
    help = """
    HELP:   show help
    LIST:   list files
    PWD:    show current dir
    CD directory_name:  change directory
    DWLD file_path:    download file
    QUIT:   exit
    """
    sock.send(str(sys.getsizeof(help)).encode())
    sock.send(help.encode())

    return


def pwd():
    # sock.send("ok".encode())

    path = os.getcwd()
    # name of root
    # print(path)
    rest = path.partition("p1")[2]
    print(f"    {rest}")
    # print(rest)
    sock.send(rest.encode())

    return


def dwld():
    sock.send("ok".encode())

    # 1
    file_name_length = int(sock.recv(1024).decode())
    file_name = sock.recv(file_name_length).decode()
    print(f"file name: {file_name}")

    # 2
    if(os.path.isfile(file_name)):
        print("exists")
        sock.send(str(os.path.getsize(file_name)).encode())
    else:
        sock.send("-1".encode())
        return

    sock.recv(1024)

    # 3
    # generate a random number bitween 3000 to 50000 for port number
    randport = random.randint(3000, 50000)
    sock.send(str(randport).encode())

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # a new tcp connection for downloading
    serverSocket.bind((server_ip, randport))
    serverSocket.listen(1)
    dwld_sock, addr = serverSocket.accept()
    print(f"new socket for downloading on port '{randport}'")

    # 4
    # sending
    print("sendin file...")
    rfile = open(file_name, "rb")
    file = rfile.read()
    dwld_sock.send(file)
    dwld_sock.recv(1024)
    rfile.close()

    # 5
    print("completed")
    dwld_sock.recv(1024)
    dwld_sock.send("close".encode())
    dwld_sock.recv(1024)
    dwld_sock.close()
    print("socket closed")
    return


while True:
    command = sock.recv(1024).decode()
    print(f"command:    {command}")

    if command == "help":
        help()
    elif command == "list":
        pass
    elif command == "pwd":
        pwd()
    elif command[0:2] == "cd":
        pass
    elif command[0:4] == "dwld":
        dwld()
    elif command == "quit":
        pass
    else:
        pass
