from socket import *

serverName = "127.0.0.1"
serverPort = 12701

ClientSocket = socket(AF_INET, SOCK_STREAM)  # TCP 연결 생성

ClientSocket.connect((serverName, serverPort))

req = ""  # 요청 문자열
buffer = []
while len(buffer)<3 or buffer[-1]:  # 길이가 2줄 이하이거나, 마지막 요청이 공백일 때까지 문자를 받습니다.
    message = input()
    if message:
        req += message
    else:
        req += '\r\n'
    buffer.append(message)
    req += '\r\n'

ClientSocket.send(req.encode())  # 요청을 보냅니다.

modifiedMessage = ClientSocket.recv(1024)  # 응답을 받고 콘솔에 출력합니다.
print(modifiedMessage.decode())

ClientSocket.close()