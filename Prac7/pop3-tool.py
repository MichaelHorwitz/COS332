import ssl
import socket
import base64
#Kivashin Naidoo u22551167
#Michael Horwitz u22512323
def make_connection():
    # Google's POP3 server details
    pop3_server = 'pop.gmail.com'
    pop3_port = 995

    # Your email credentials
    username = 'kivashin332@gmail.com'
    password = 'txqd dgkc dqcf xfpn'

    pop3_socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    pop3_socket.connect((pop3_server, pop3_port))

    print(pop3_socket.recv(1024).decode())

    pop3_socket.sendall(f'USER {username}\r\n'.encode())
    print(pop3_socket.recv(1024).decode())

    pop3_socket.sendall(f'PASS {password}\r\n'.encode())
    print(pop3_socket.recv(1024).decode())

    return pop3_socket

def count_mail(pop3_socket):
    print("POP3 command being used: LIST")
    pop3_socket.sendall(b'LIST\r\n')
    mail_list = pop3_socket.recv(1024).decode()
    split_list = mail_list.split(' ')
    number_of_mails = split_list[1]
    print("You currently have "+ number_of_mails +" emails in the inbox")
    
    return int(number_of_mails)

def check_bcc_count(pop3_socket, number_of_mails):
    count = 0
    i = number_of_mails
    for x in range(1, number_of_mails+1):
        req_string = "RETR "+str(x)
        pop3_socket.sendall(req_string.encode() + b'\r\n')
        email_content = ''
        print_content = False
        while True:
            # print("Reading email")
            line = pop3_socket.recv(1024).decode()
            email_string = line.strip()
            start_index = email_string.find("MIME-Version:")
            end_index = email_string.find("Content-Type: text/plain;")
            if start_index != -1 and end_index != -1:
                email_content+=email_string[start_index:end_index]
                print("=============START OF HEADER============")
                print(email_content)
                print("=============END OF HEADER==============")
                if email_content.find("Bcc: ") != -1 :
                    count = count+1
                break
            elif start_index != -1:
                print_content = True
                email_content+=email_string[start_index:]
            elif end_index != -1:
                print_content = False
                email_content+=email_string[:end_index]
                print("=============START OF HEADER============")
                print(email_content)
                print("=============END OF HEADER==============")
                if email_content.find("Bcc: ") != -1 :
                    count = count+1
                break
            elif email_string.find("by smtp")!=-1:
                print_content = True
                email_content+=email_string
                print("=============START OF HEADER============")
                print(email_content)
                print("=============END OF HEADER==============")
                break
            if print_content == True:
                email_content+=email_string
            # print(email_string)
                       
    print("You have been BCC'd "+str(count)+" times")
    return count

def send_notification_email():
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

    smtp_socket.sendall(b'To: <kivashin332@gmail.com>\r\nSubject: BCC WARNING!!!\r\n\r\nHey there you not so competent person, just a warning that you have been BCCd so reply carefully :D\r\n.\r\n')
    print(smtp_socket.recv(1024).decode())
    print("Warning email sent!")

pop3_socket = make_connection()
num_mails = count_mail(pop3_socket)
bcc_count = check_bcc_count(pop3_socket, num_mails)
pop3_socket.close()
if bcc_count > 0:
    send_notification_email()
