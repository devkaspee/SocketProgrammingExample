from socket import *
import sys
from time import sleep

# Input Server IP ####################
serverIp = "192.168.123.150"
######################################

serverSocket = socket(AF_INET, SOCK_STREAM)  # 기본적인 조합 (생략 가능)
serverPort = 12001
# serverIp = "192.168.123.150"

serverSocket.bind((serverIp, serverPort))  # IP와 Port 를 바인드함
serverSocket.listen(1)  # 대기 상태로 전환
serverSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, True) # 즉시 처리
cnt = 5  # 서버에서 처리할 수 있는 최대 전송량

HTTP_METHOD = ["GET", "POST", "HEAD"]  # 해당 웹서버가 처리할 수 있는 Method

HTTP_BODY = "\r\n<html><body><h1>Hello, world!</h1>\n" \
            "<p>This Page is Virtual Page" \
            "</body></html>"                    # 서버가 가지고 있는 http 객체

RES_Hdr = "Cotent-Length: 349\r\nContent-Type: text/html\r\n"  # 서버에서 보낼 응답 헤더

S_dir = ['/', '/admin']  # 해당 웹서버가 가지고 있는 객체의 디렉토리

Stime = 10  # 요청 객체가 수정된 마지막 시간 (If-Modified-Since 를 위함)
HTMLreturn = True  # 객체를 전송할 것인지 결정함

while cnt:
    print("The server is ready to receive")

    # Set Up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
    HTMLreturn = True                               # 변수 초기화
    req = ""                                        # 변수 초기화
    message = connectionSocket.recv(1024).decode()  # 메세지 수신
    if not(message):
        connectionSocket.send("Please Retry Send".encode())
        print(message+" 빈 문자열이 도달했습니다.")
        continue

    if len(message.split()) >= 3:  # 첫 줄의 길이가 충분한지 판단
        reqMethod, reqDir, reqFor = map(str, [message.split()[i] for i in range(3)])
    else :
        req = "HTTP/1.0 501 Not Implemented"  # 부적절한 요청
        connectionSocket.send(req.encode())
        continue

    if len(message.strip().split('\r\n')) < 2:
        req = "HTTP/1.0 501 Not Implemented"  # 부적절한 요청
        connectionSocket.send(req.encode())
        continue

    if not req and (reqMethod not in HTTP_METHOD):  # 첫 줄의 요청 Method 를 서버가 처리할 수 있는지 판단
        req = reqFor + " 400 Bad request"

    if not req and reqMethod == 'HEAD':  # 해당 요청이 HEAD 인지 판단
        HTMLreturn = False

    if not req and reqDir not in S_dir:  # 해당 요청에 해당하는 객체가 서버 디렉토리에 존재하는지 판단
        req = reqFor+" 404 Not Found"

    if not req and reqDir == '/admin':  # 해당 요청에 권한이 있는지 판단 (여기서는 모든 유저가 권한이 없다고 설정)
        req = reqFor+" 403 Forbidden"

    tmp = message.rstrip().split('\r\n')[1:]  # 헤더 목록을 파싱
    reqHddr = {}                  # 헤더: 값 쌍으로 삽입 {'Host': '123.213.123.112', 'If-Modified-Since': '213', 'Text': '2132'}
    for i in range(len(tmp)):
        try:
            reqHddr[tmp[i].split(":")[0].strip()] = tmp[i].split(':')[1].strip()
        except:
            continue

    if "If-Modified-Since" in reqHddr.keys():  # If-Modified-Since 헤더 검사
        try:
            if (int(reqHddr["If-Modified-Since"]) >= 10):
                req = reqFor + " 304 Not Modified"  # 위에서 참이면, 304 코드와 함께, 객체를 보내지 않음
                HTMLreturn = False
        except:
            pass


    if "Host" in reqHddr.keys() or "host" in reqHddr.keys():  # Host 헤더 검사 (필수)
        try:
            if "Host" in reqHddr.keys():
                if reqHddr["Host"].rstrip() != serverIp:
                    req = reqFor + " 400 Bad request"
            else:
                if reqHddr["host"].rstrip() != serverIp:
                    req = reqFor + " 400 Bad request"
        except:
            pass

    else:
        req = reqFor + " 400 Bad request"

    if not req:
        req = reqFor+" 200 OK"  # 위에서 모두 이상이 없다면 200 OK로 객체 전송

    req += "\r\nDate: Sun, 13 Jan 2019 17:28:13 GMT\r\n" + (RES_Hdr if HTMLreturn else "") + "\r\n" # 응답 헤더 필드를 메세지에 삽입
    if HTMLreturn:
        req+= HTTP_BODY  # HTTP 객체를 삽입
    connectionSocket.sendall((req).encode())  # 보냄
    if connectionSocket.recv(1024).decode().strip() == "Bye":
        print("Disconnected from Client")

        connectionSocket.close()
    cnt -= 1

serverSocket.close()
sys.exit()
