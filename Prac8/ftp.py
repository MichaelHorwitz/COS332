import socket

HOST = '127.0.0.1'
PORT = 21

def myPrint(byteStr):
    if not isinstance(byteStr, bytes):
        byteStr = bytes(byteStr, 'UTF-8')
    print(str(byteStr.decode('UTF-8')))

class ftpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def connectToServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ftpSocket:
            self.ftpSocket.connect((self.host, self.port))
            initResponse = self.ftpSocket.recv(1024)
            myPrint(initResponse)
            self.login()
    def login(self):
        requests = ['USER testftp', 'PASS 1234']
        for request in requests:
            self.ftpSocket.send(bytes(request + '\r\n','UTF-8'))
            print(request)
            response = self.ftpSocket.recv(1024)
            myPrint(response)
ftp = ftpClient(HOST, PORT)
ftp.connectToServer()
            

