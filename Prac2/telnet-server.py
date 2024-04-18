import random
import socket
# Michael Horwitz u22512323
# Kivashin Naidoo u22551167
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
    clientSocket, address = telSock.accept()
    score = 0
    with clientSocket:
        continueLoop = True
        while continueLoop:
            clientSocket.sendall(b"\033[2J")
            char = ord('A')
            currQuestion = random.choice(questions)
            displayStr = currQuestion.text
            for ans in currQuestion.answerList:
                displayStr += chr(char)
                char += 1
                displayStr += " " + ans.text
            displayStr += "\n"
            # when connected say hello world
            # b indicates a byte like string
            clientSocket.sendall(bytes(displayStr, "utf-8"))
            # wait for input
            cmd = clientSocket.recv(1024)
            correctAns = False
            cmdText = cmd.decode("utf-8").strip().upper()[0]
            cmdNum = ord(cmdText) - ord('A')
            if currQuestion.answerList[cmdNum].isCorrect:
                clientSocket.sendall(b"Good Job!!\n")
                score += 1
            else:
                for ans in currQuestion.answerList:
                    if ans.isCorrect:
                        correction = "The correct answer was:" + ans.text
                        clientSocket.sendall(bytes(correction, "utf-8"))
            # for ans in currQuestion.answerList:
            #     if ans.isCorrect:
            #         cmdText = cmd.decode("utf-8").strip()
            #         cmdText = cmdText
            #         ansBytes = bytes(ans.text, "utf-8")
            #         #print(f"cmdText {cmdText}")
            #         #print(cmd)
            #         #print(f'ansBytes {ansBytes}')

            #         if ans.text.strip() == cmdText.strip():
            #             correctAns = True
            #         else:
            #             correctAns = False
            #             correction = ans.text
            # if correctAns:
            #     clientSocket.sendall(b"Good Job!!")
            # else:
            #     correction = "The correct answer was " + correction
            #     clientSocket.sendall(bytes(correction, "utf-8"))
            clientSocket.sendall(b"Would you like to play again? (y/N)\n")
            cmd = clientSocket.recv(1024)
            continueLoop = cmd.decode("utf-8").strip() == "y"
        clientSocket.sendall(b"Score:")
        clientSocket.sendall(bytes(str(score) + "\n", "utf-8"))
        clientSocket.close()
