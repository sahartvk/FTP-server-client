import socket

server_ip = '127.0.0.1'
server_port = 1234

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting...")
clientSocket.connect((server_ip, server_port))
print("connected to server successfully")

help_size = int(clientSocket.recv(4).decode())
help = clientSocket.recv(help_size).decode()
print(help)
