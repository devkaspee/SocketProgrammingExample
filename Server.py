from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)  # 기본적인 조합 (생략 가능)
serverPort = 12701
serverSocket.bind(("127.0.0.1", serverPort))  # IP와 Port 를 바인드함
serverSocket.listen(1)  # 대기 상태로 전환

cnt = 5  # 서버에서 처리할 수 있는 최대 전송량

HTTP_METHOD = ["GET", "POST", "HEAD"]  # 해당 웹서버가 처리할 수 있는 Method
HTTP_BODY = "<html><body><h1>Hello, world!</h1>\n" \
            "<p>This Page is Virtual Page" \
            "</body></html>"
RES_Hdr = "\r\nCotent-Length: 349\r\nContent-Type: text/html\r\n"
S_dir = ['/', '/admin']  # 해당 웹서버가 가지고 있는 객체의 디렉토리 주소

Stime = 10  # 요청 객체가 수정된 마지막 시간 (If-Modified-Since 를 위함)
HTMLreturn = True  # 객체를 전송할 것인지 결정함

while cnt:
    print("The server is ready to receive")

    # Set Up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    HTMLreturn = True
    req = ""
    message = connectionSocket.recv(1024).decode()
    if not(message):
        connectionSocket.send("Please Retry Send".encode())
        print(message+" OMG:::")
        continue

    if len(message.split()) >= 3:  # 첫 줄의 길이가 충분한지 판단
        reqMethod, reqDir, reqFor = map(str, [message.split()[i] for i in range(3)])
    else :
        req = "HTTP/1.0 501 Not Implemented"  # 부적절한 요청
        connectionSocket.send(req.encode())
        continue

    if not req and (reqMethod not in HTTP_METHOD):  # 첫 줄의 요청 Method 를 서버가 처리할 수 있는지 판단
        req = reqFor + " 400 Bad request"

    if not req and "Host" not in message.split():  # 헤더에 Host 필드가 들어있는지 판단
        req = reqFor + " 400 Bad request"

    if not req and reqMethod == 'HEAD':  # 해당 요청이 HEAD 인지 판단
        HTMLreturn = False

    if not req and reqDir not in S_dir:  # 해당 요청에 해당하는 객체가 서버 디렉토리에 존재하는지 판단
        req = reqFor+" 404 Not Found"

    if not req and reqDir == '/admin':  # 해당 요청에 권한이 있는지 판단 (여기서는 모든 유저가 권한이 없다고 설정)
        req = reqFor+" 403 Forbidden"

    reqHddr = message.split('\r\n')[1:]  # 헤더 목록을 파싱

    for i in range(len(reqMethod)):
        if len(reqHddr[i]) >= len("If-Modified-Since") and "If-Modified-Since" in reqHddr[i]:  # 특정 헤더가 있는지 판단
            try:
                tmp = int(reqHddr[i][reqHddr[i].index(":")+1:])  # 있다면, 필드의 Value 를 확인 ( Integer 값만 받음)

            except:
                break
            if tmp >= 10:                     # 해당 객체가 수정된 시간이 Value 보다 전인지 판단
                req = reqFor+" 304 Not Modified"  # 위에서 참이면, 304 코드와 함께, 객체를 보내지 않음
                HTMLreturn = False


    if not req:
        req = reqFor+" 200 OK"  # 위에서 모두 이상이 없다면 200 OK로 객체 전송

    req += RES_Hdr  # 응답 헤더 필드를 메세지에 삽입
    if HTMLreturn:
        req+= HTTP_BODY  # HTTP 객체를 삽입

    connectionSocket.send((req).encode())  # 보냄

    connectionSocket.close()  # 요청을 끝낸다
    cnt -= 1

serverSocket.close()
sys.exit()