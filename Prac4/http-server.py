from calendar import c
import random
import socket
# Michael Horwitz u22512323
# Kivashin Naidoo u22551167
formFormat = f"""HTTP/1.1 200 OK
Content-Type: text/html
Cache-Control: no-cache

<!DOCTYPE html>
<body>
    {{mainBody}}
    <form method="get" accept-charset=utf-8 action="http://localhost:{{PORT}}/">
        {{questionText}}<br>
        {{inputs}}
        <input type="hidden" value="">
        <input type="submit" value="Answer">
    </form>
</body>"""
inputFormat = f'<input type="radio" name="answer" value="{{letter}}" size="20">{{answerText}}<br>'
hiddenInputFormat = f'<input type="hidden" name="{{name}}" value="{{correctAnsNum}}">'
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
    output = formFormat.format(questionText=currQuestion.text, inputs = inputStr, PORT=PORT, mainBody="")
    #print(output)
    clientSocket.sendall(bytes(output, "utf-8"))
    
def sendResponseForm(getParams):
    getParams = getParams[1:]
    fields = getParams.split('&')
    
    currScore = fields[2].split('=')[1]
    
    if fields[0].split('=')[1] == fields[1].split('=')[1]:
        mainBody ="CORRECT"
        currScore = int(currScore) + 1
    else:
        mainBody = "INCORRECT"
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

def default_favicon_response():
    response = 'HTTP/1.1 200 OK\n'
    response += 'Content-Type: image/x-icon\n\n'
    clientSocket.sendall(bytes(response, "utf-8"))

def processRequest(request):
    print("###################")
    print(request)
    headers = request.split('\n')
    #print('Headers[0]\n' + headers[0])
    getParams = headers[0].split()[1]
    #print(getParams)
    print('******************')
    if getParams == '/':
        #print(request)
        sendQuestionForm()
        return
    if "favicon.ico" in getParams:
        default_favicon_response()
        return
    sendResponseForm(getParams)

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