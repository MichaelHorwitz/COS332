from re import split
import socket
import hashlib

HOST = '127.0.0.1'
PORT = 21

def myPrint(byteStr):
    if not isinstance(byteStr, bytes):
        byteStr = bytes(byteStr, 'UTF-8')
    print(str(byteStr.decode('UTF-8')))

class ftpClient:
    def __init__(self, inSocket):
        self.ftpSocket = inSocket
    def connectToServer(self):
        self.ftpSocket.connect((HOST, PORT))
        initResponse = self.ftpSocket.recv(1024)
        myPrint(initResponse)
        self.login()
    def login(self):
        requests = ['USER testftp', 'PASS 1234']
        self.doRequests(requests)
        
    def checkStatus(self):
        request = "STAT"
        self.ftpSocket.send(bytes(request + '\r\n','UTF-8'))
        print(request)
        response = self.ftpSocket.recv(1024)
        myPrint(response)
        if response[:3] != b'211':
            return False
        return True
    
    def doRequests(self, listOfRequests):
        for request in listOfRequests:
            self.ftpSocket.send(bytes(request + '\r\n','UTF-8'))
            print(request)
            response = self.ftpSocket.recv(1024)
            myPrint(response)
    def getFile(self, fileStr):
        #request = bytes('RETR ' + fileStr + '\r\n', 'UTF-8')
        request = 'EPSV'
        # request = 'PASV'
        myPrint(request)
        self.ftpSocket.send(bytes(request + '\r\n','UTF-8'))
        response =self.ftpSocket.recv(1024)
        myPrint(response)
        # check response code
        #print(response[:3])
        if response[:3] == b'226':
            myPrint(request)
            self.ftpSocket.send(bytes(request + '\r\n','UTF-8'))
            response =self.ftpSocket.recv(1024)
            myPrint(response)
            
        response = response.decode('UTF-8')
        newPort = response.split(' ')[-1]
        newPort = newPort[4:9]
        print(newPort)
        newPort = int(newPort)
        globalNewPort = newPort
        newPort = globalNewPort
        self.doRequests(['RETR ' + fileStr])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as fileSocket:
            fileSocket.connect((HOST, newPort))
            response = fileSocket.recv(1024)
            response = response.decode('UTF-8')
            # self.doRequests(['EPSV'])
            EPSVresponse =self.ftpSocket.recv(1024)
            myPrint(EPSVresponse)
            return response
    def checkDiffFiles(self, file1, file2):
        # open file called file2 and read into string
        # check if there is a file called file2
        try:
            with open(file2, 'r') as file:
                file2Str = file.read()
            #create a md5 hash of fileStr2
            file2Hash = hashlib.md5(bytes(file2Str, "UTF-8")).hexdigest()
            with open("hash_" + file2, 'r') as file:
                file2HashFile = file.read()
            # if file1Str == file2Str:
            # print(file2Hash)
            # print(file2HashFile)
            if file2Hash == file2HashFile:
                return "File is protected"
        except FileNotFoundError:
            pass
        if not self.checkStatus():
            return "Server not ready"
        file1Str = self.getFile(file1)
        file1Str = file1Str.split('\r\n')[0]
        file1Hash = self.getFile("hash_" + file1)
        file1Hash = file1Hash.split('\r\n')[0]
        with open(file2, 'w') as file:
            file.write(file1Str)
        with open("hash_" + file2, 'w') as file:
            file.write(file1Hash)
        return "Restored old file"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ftpSocket:
    ftp = ftpClient(ftpSocket)
    ftp.connectToServer()
    #ftp.getFile('test.txt')
    # repeat every 5 seconds
    ftp.appendToLog("HELLO")
    while True:
        print(ftp.checkDiffFiles('test.txt', 'test.txt'))
        import time
        time.sleep(5)
            

