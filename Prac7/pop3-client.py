import ssl
import socket

#Kivashin Naidoo u22551167
#Michael Horwitz u22512323

# Google's POP3 server details
pop3_server = 'pop.gmail.com'
pop3_port = 995

#Email credentials
username = 'kivashin332@gmail.com'
password = 'txqd dgkc dqcf xfpn'

# Connect to the POP3 server using SSL/TLS
pop3_socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
pop3_socket.connect((pop3_server, pop3_port))

# Receive the server's greeting
print(pop3_socket.recv(1024).decode())

# Send the username
pop3_socket.sendall(f'USER {username}\r\n'.encode())
print(pop3_socket.recv(1024).decode())

# Send the password
pop3_socket.sendall(f'PASS {password}\r\n'.encode())
print(pop3_socket.recv(1024).decode())

# Loop to interact with the server
while True:
    # Input POP3 command
    command = input("Input POP3 command: ")
    pop3_socket.sendall(command.encode() + b'\r\n')
    response = pop3_socket.recv(1024).decode()
    if not command.startswith("RETR"): print(response)
    
    if command.startswith("RETR"):
        # Read the content of the email
        email_content = ''
        print_content = False

        while True:
            line = pop3_socket.recv(1024).decode()
            email_string = line.strip()
            print(email_string)
            # start_index = email_string.find("MIME-Version:")
            # end_index = email_string.find("Content-Type:")
            # if start_index != -1 and end_index != -1:
            #     email_content+=email_string[start_index:end_index]
            #     print("=============START OF HEADER============")
            #     print(email_content)
            #     print("=============END OF HEADER==============")
            #     break
            # elif start_index != -1:
            #     print_content = True
            #     email_content+=email_string[start_index:]
            # elif end_index != -1:
            #     print_content = False
            #     email_content+=email_string[:end_index]
            #     print("=============START OF HEADER============")
            #     print(email_content)
            #     print("=============END OF HEADER==============")
            #     break
            # if print_content == True:
            #     email_content+=email_string
                
            
    if command == "QUIT":
        break

# Close the connection
pop3_socket.close()
