from calendar import c
import random
import socket
# Michael Horwitz u22512323
# Kivashin Naidoo u22551167
finishedString = f"""HTTP/1.1 200 OK
Content-Type: text/html
Cache-Control: no-cache

<!DOCTYPE html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
</head>
<body><h1>{{content}}</h1></body>
"""
formFormat = f"""HTTP/1.1 200 OK
Content-Type: text/html
Cache-Control: no-cache

<!DOCTYPE html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
</head>
<body>
    {{mainBody}}
    <form method="post" accept-charset=utf-8 action="http://localhost:{{PORT}}/">
        {{questionText}}<br>
        {{inputs}}
        <input type="submit" name="answerButton" value="Answer">
        {{finishButton}}
    </form>
</body>"""
inputFormat = f'<input type="radio" name="answer" value="{{letter}}" size="20">{{answerText}}<br>'
hiddenInputFormat = f'<input type="hidden" name="{{name}}" value="{{correctAnsNum}}">'
finishButton = '<input type="submit" name="finishButton" value="finish">'
class Answer:
    def __init__(self, text, isCorrect):
        self.text = text
        self.isCorrect = isCorrect

class Question:
    def __init__(self, text):
        self.text = text
        self.answerList = []
    def addAnswer(self, answer):
        self.answerList.append(answer)
    def hasCorrectAnswer(self):
        for answer in self.answerList:
            if answer.isCorrect:
                return True
        return False
    def findCorrectAnswer(self):
        self.correctAnsNumArr = []
        i = 0
        for answer in self.answerList:
            if answer.isCorrect:
                self.correctAnsNumArr.append(i)
            i = i + 1

def sendQuestionForm():
    currQuestion = random.choice(questions)
    char = ord('0')
    inputStr = ""
    for ans in currQuestion.answerList:
        inputStr += inputFormat.format(letter=chr(char), answerText=ans.text)
        char += 1
    for num in currQuestion.correctAnsNumArr:
        inputStr += hiddenInputFormat.format(name="correctAnsNum", correctAnsNum=num)
    inputStr += hiddenInputFormat.format(name="score", correctAnsNum='0')
    inputStr += hiddenInputFormat.format(name="totalQuestions", correctAnsNum='1')
    output = formFormat.format(questionText=currQuestion.text, inputs = inputStr, PORT=PORT, mainBody="", finishButton="")
    clientSocket.sendall(bytes(output, "utf-8"))
    
def sendResponseForm(getParams):
    getParams = getParams[1:]
    fields = getParams.split('&')
    
    currScore = fields[2].split('=')[1]
    
    if fields[0].split('=')[1] == fields[1].split('=')[1]:
        mainBody ="<h1>CORRECT"
        currScore = int(currScore) + 1
    else:
        mainBody = "<h1>INCORRECT"
    mainBody += "SCORE: " + str(currScore) + "<br>"

    currQuestion = random.choice(questions)
    char = ord('0')
    inputStr = ""
    for ans in currQuestion.answerList:
        inputStr += inputFormat.format(letter=chr(char), answerText=ans.text)
        char += 1
    for num in currQuestion.correctAnsNumArr:
        inputStr += hiddenInputFormat.format(name="correctAnsNum", correctAnsNum=num)
    inputStr += hiddenInputFormat.format(name="score", correctAnsNum=str(currScore))
    output = formFormat.format(questionText=currQuestion.text, inputs = inputStr, PORT=PORT, mainBody=mainBody)
    #print(output)
    clientSocket.sendall(bytes(output, "utf-8"))

def postResponseForm(postParamPairs):
    
    currScore = postParamPairs[2][1]
    totalQuestions = int(postParamPairs[3][1])
    
    if postParamPairs[0][1] == postParamPairs[1][1]:
        mainBody ="<h1>CORRECT<br>"
        currScore = int(currScore) + 1
    else:
        mainBody = "<h1>INCORRECT<br>"
    mainBody += "SCORE: " + str(currScore) + "/" + str(totalQuestions)+ "</h1>"

    currQuestion = random.choice(questions)
    char = ord('0')
    inputStr = ""
    for ans in currQuestion.answerList:
        inputStr += inputFormat.format(letter=chr(char), answerText=ans.text)
        char += 1
    for num in currQuestion.correctAnsNumArr:
        inputStr += hiddenInputFormat.format(name="correctAnsNum", correctAnsNum=num)
    inputStr += hiddenInputFormat.format(name="score", correctAnsNum=str(currScore))
    inputStr += hiddenInputFormat.format(name="totalQuestions", correctAnsNum=str(totalQuestions + 1))
    output = formFormat.format(questionText=currQuestion.text, inputs = inputStr, PORT=PORT, mainBody=mainBody, finishButton=finishButton)
    clientSocket.sendall(bytes(output, "utf-8"))

def default_favicon_response():
    response = 'HTTP/1.1 200 OK\n'
    response += 'Content-Type: image/x-icon\n\n'
    clientSocket.sendall(bytes(response, "utf-8"))

def processRequest(request):
    print("###################")
    print(request)
    headers = request.split('\n')
    #print('Headers[0]\n' + headers[0])
    if headers[0].split()[0] == 'GET':
        #print('GETTEEEMMM')
        getParams = headers[0].split()[1]
        print(getParams)
        print('******************')
        if getParams == '/':
            #print(request)
            sendQuestionForm()
            return
        if "favicon.ico" in getParams:
            default_favicon_response()
            return
        sendResponseForm(getParams)
    elif headers[0].split()[0] == 'POST':
        #print('POOOOOOOOOOOOOOST')
        postParamLine = headers[-1]
        postParams = postParamLine.split('&')
        postParamPairs = []
        for pair in postParams:
            postParamPairs.append(pair.split('='))
        if postParamPairs[0][0] != 'answer':
            postParamPairs.insert(0, ['answer', '-1'])
        if postParamPairs[4][0] == "answerButton":
            return postResponseForm(postParamPairs)
        postParamPairs[3][1] = str(int(postParamPairs[3][1]) - 1)
        content = str(postParamPairs[2][1]) + "/" + str(postParamPairs[3][1])
        content = "Final Score: " + content + "<br>Check your emails for a summary"
        clientSocket.sendall(bytes(finishedString.format(content=content), 'UTF-8'))
        finalStr = 'You scored: ' + postParamPairs[2][1] + '/' + postParamPairs[3][1]
        sendEmail(bytes(finalStr, 'UTF-8'))

            
        
#initialise questions
questions = []
with open("questions.txt", "r") as file:
    for line in file:
        if line[0] == "?":
            questions.append(Question(line[1:]))
        if line[0] == "-":
            questions[-1].addAnswer(Answer(line[1:], False))
        if line[0] == "+":
            questions[-1].addAnswer(Answer(line[1:], True))
for curr in questions:
    numCorrect = 0
    for ans in curr.answerList:
        if ans.isCorrect:
            numCorrect += 1
    if numCorrect == 0:
        curr.addAnswer(Answer("None of the above", True))
    if numCorrect > 1:
        for ans in curr.answerList:
            ans.isCorrect = False
        curr.addAnswer(Answer("More than one of the above", True))
for curr in questions:
    curr.findCorrectAnswer()

def sendEmail(bodyText):
    SMTP_PORT = 25
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as emailSocket:
        standardRequests = [b'HELO example.com\r\n',
                            b'VRFY michl\r\n',
                            b'MAIL FROM:me@example.com\r\n', 
                            b'RCPT TO:michael@localhost.localdomain\r\n', 
                            b'DATA\r\n',
                            ]
        subjectLine = b'Subject: Test Results\r\n'
        bodyText += b'\r\n.\r\n'
        bodyText = subjectLine + bodyText
        standardRequests.append(bodyText)
        # bind and listen on emailSocket
        emailSocket.connect((HOST, SMTP_PORT))
        response = emailSocket.recv(1024)
        print("RECEIVED: ", str(response))

        
        for request in standardRequests:
            emailSocket.send(request)  
            print("SENT: ", str(request))
            
            response = emailSocket.recv(1024)
            print("RECEIVED: ", str(response))
            responseCode = str(response).split()[0]
            responseCode = responseCode[2:]
            if request == standardRequests[1]:
                if responseCode == '550':
                    emailSocket.send(b'QUIT\r\n')
                    #emailSocket.send(request)  
                    print("SENT: ", str(request))
            
                    response = emailSocket.recv(1024)
                    print("RECEIVED: ", str(response))
                    return
            
                    
                

PORT = 55555
HOST = "127.0.0.1"

# https://realpython.com/python-sockets/
# AF_INET = IPv4
# SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as telSock:
    # bind and listen on telSock
    telSock.bind((HOST, PORT))
    telSock.listen()
    print(f"listening on port {PORT}")
    # wait for a client to connect
    
    score = 0
    stillPlaying = True
    while stillPlaying:
        clientSocket, address = telSock.accept()
        with clientSocket:
            request = clientSocket.recv(1024).decode()
            processRequest(request)