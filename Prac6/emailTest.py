import socket

PORT = 25
HOST = "127.0.0.1"

def sendEmail(bodyText):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as emailSocket:
        standardRequests = [b'HELO example.com\r\n', 
                            b'MAIL FROM:me@example.com\r\n', 
                            b'RCPT TO:michael@localhost.localdomain\r\n', 
                            b'DATA\r\n',
                            ]
        bodyText += b'\r\n.\r\n'
        standardRequests.append(bodyText)
        # bind and listen on emailSocket
        emailSocket.connect((HOST, PORT))
        
        for request in standardRequests:
            emailSocket.send(request)    
            print("SENT: ", request)
            
            response = emailSocket.recv(1024)
            print("RECEIVED: ", response)
sendEmail(b'Does my function work?')