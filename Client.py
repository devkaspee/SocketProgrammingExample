from socket import *
import time


# Input Server IP & Port #############
serverName = "192.168.123.150"
serverPort = 12001
######################################

ClientSocket = socket(AF_INET, SOCK_STREAM)  # TCP 연결 생성
ClientSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
ClientSocket.connect((serverName, serverPort))

req = ""  # 요청 문자열
buffer = []  # 라인이 몇 개인지 세기 위한 리스트
while len(buffer)<3 or buffer[-1]:  # 길이가 3줄 이상이거나, 마지막 요청이 공백일 때까지 문자를 받습니다.
    message = input()
    if message:
        req += message              # request message에 추가
    else:
        req += '\r\n'               # 그냥 줄만 넘김
    buffer.append(message)
    req += '\r\n'

ClientSocket.send(req.encode())  # 요청을 보냅니다.

modifiedMessage = ClientSocket.recv(1024)  # 응답을 받고 콘솔에 출력합니다.
print(modifiedMessage.decode())
ClientSocket.send("Bye".encode())


ClientSocket.shutdown(1)
ClientSocket.close()
