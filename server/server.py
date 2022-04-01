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
    path=str(os.getcwd().partition("FTP-server-client")[2])
    sock.send(str(sys.getsizeof(path)).encode())
    sock.send(path.encode())
    print(f"{path}")
    print("Successfully sent directory \n")
    return

def size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for i in filenames:
            f = os.path.join(dirpath, i)
            total_size += os.path.getsize(f)
    return total_size


def list():
    sock.send("ok".encode())

    temp = ""
    total_size = 0
    with os.scandir(os.getcwd()) as entries:
        for entry in entries:
            if entry.is_dir():
                temp += " ￿ "
                temp += str(entry.name)
                temp += "     "
                temp += str(size(os.path.join(os.getcwd(), entry)))
                temp += "\n"
                total_size += size(os.path.join(os.getcwd(), entry))

            elif entry.is_file():
                temp += "   "
                temp += str(entry.name)
                temp += "     "
                temp += str(os.path.getsize(entry))
                temp += "\n"
                total_size += os.path.getsize(entry)

    
    sock.send(str(len(temp.encode('utf-8'))).encode())
    sock.send(temp.encode())
    sock.send(str(total_size).encode())
    return


def cd():
    sock.send("ok".encode())

    directory = sock.recv(1024).decode()

    path = os.getcwd()
    print(f" current path : {path}")

    if os.path.isdir(os.path.join(path, directory)):
        os.chdir(os.path.join(path, directory))
        sock.send("changed".encode())
    else:
        print("invalid directory")
        sock.send("invalid".encode())

    path = os.getcwd()
    print(f" current path : {path}")


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
    print(command)

    if command == "help":
        help()
    elif command == "list":
        list()
    elif command == "pwd":
        pwd()
    elif command[0:2] == "cd":
        cd()
    elif command[0:4] == "dwld":
        dwld()
    elif command == "quit":
        print("exiting ...")
        sock.close()
        break
    else:
        print("....")
