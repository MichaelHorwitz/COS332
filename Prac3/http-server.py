import socket
# Michael Horwitz u22512323
# Kivashin Naidoo u22551167
def is_port_available(port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as portSocket:
    try:
      portSocket.bind((HOST, port))
      return True
    except OSError:
      return False

# Michael Horwitz u22512323
# Kivashin Naidoo u22551167
HOST = "127.0.0.1"
PORT = 55555  # Starting port

# Find the next available port
while not is_port_available(PORT):
  PORT += 1  # Increment port number until available


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as telSock:
    # bind and listen on telSock
    telSock.bind((HOST, PORT))
    telSock.listen()
    print(f"listening on port {PORT}")
    # wait for a client to connect
    clientSocket, address = telSock.accept()
    with clientSocket:
        request = clientSocket.recv(1024)
        request = str(request)
        requestSplit = request.split('\\r\\n')
        for i in range(len(requestSplit)):
          requestSplit[i] = requestSplit[i].split()
        response = 'HTTP/1.1 200 OK\r\n\Content-Type: text/html\r\n\r\n'
        print(requestSplit)
        #print(request)
        clientSocket.sendall(bytes(response, 'UTF-8'))