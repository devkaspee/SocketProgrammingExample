from socket import *

serverName = "127.0.0.1"
serverPort = 12701

# Create a TCP client socket

ClientSocket = socket(AF_INET, SOCK_STREAM)
try:
    ClientSocket.connect((serverName, serverPort))
except:
    ClientSocket.connect((serverName, serverPort+1))
req = ""
buffer = []
while len(buffer)<3 or buffer[-1]:
    message = input()
    if message:
        req += message
    else:
        req += '\r\n'
    buffer.append(message)
    req += '\r\n'


ClientSocket.send(req.encode())

modifiedMessage = ClientSocket.recv(1024)
print(modifiedMessage.decode())

ClientSocket.close()