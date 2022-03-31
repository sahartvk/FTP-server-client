import socket
import sys


server_ip = '127.0.0.1'
server_port = 1234

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((server_ip, server_port))
print("listening...")
serverSocket.listen(5)

sock, addr = serverSocket.accept()
print(f"client connected by address {addr}")

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
