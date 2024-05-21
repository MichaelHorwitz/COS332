import socket
import ssl
import base64
import ssl
#Kivashin Naidoo u22551167
#Michael Horwitz u22512323
smtp_server = 'smtp.gmail.com'
smtp_port = 465
username = 'kivashin332@gmail.com'
password = 'txqd dgkc dqcf xfpn'

# Create a default SSL context for a client
context = ssl.create_default_context()

# Create a socket, wrap it with SSL/TLS, and connect to the server
smtp_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=smtp_server)
smtp_socket.connect((smtp_server, smtp_port))

smtp_socket.sendall(b'EHLO example.com\r\n')
print(smtp_socket.recv(1024).decode())

smtp_socket.sendall(b'AUTH LOGIN\r\n')
print(smtp_socket.recv(1024).decode())

smtp_socket.sendall(base64.b64encode(username.encode()) + b'\r\n')
print(smtp_socket.recv(1024).decode())

smtp_socket.sendall(base64.b64encode(password.encode()) + b'\r\n')
print(smtp_socket.recv(1024).decode())

smtp_socket.sendall(b'MAIL FROM:<kivashin332@gmail.com>\r\n')
print(smtp_socket.recv(1024).decode())

smtp_socket.sendall(b'RCPT TO:<kivashin332@gmail.com>\r\n')
print(smtp_socket.recv(1024).decode())

smtp_socket.sendall(b'DATA\r\n')
print(smtp_socket.recv(1024).decode())

smtp_socket.sendall(b'To: <kivashin332@gmail.com>\r\nSubject: TESTING SMTP\r\n\r\nHi there, a test email this is!\r\n.\r\n')
print(smtp_socket.recv(1024).decode())

print("Communication finished")
