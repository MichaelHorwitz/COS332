#!/usr/local/bin/python3
import os
# Open the file and convert list to ints
file = open("numbers.txt", "r")
numberList = file.read().split()
for i in range(3):
    numberList[i] = int(numberList[i])

# Get the query and extract the specific function
# Assumes that the query will follow the format func=XXXX
# Can do input validation but not required for this program
qString = os.environ.get('QUERY_STRING')
if len(qString) > 5:
    qString = qString[5:]

# Change the numbers and store whether or not numbers were changed
changed = False
if qString == "next":
    for i in range(2):
        numberList[i] = numberList[i + 1]
    numberList[2] = numberList[0] + numberList[1]
    changed = True
elif qString == "prev":
    for i in range(2, 0, -1):
        numberList[i] = numberList[i - 1]
    numberList[0] = numberList[2] - numberList[1]
    changed = True
lower = False
if numberList[1] == 0:
    lower = True
print("Content-Type: text/html\n")
print('<html>')
print('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>')
print('<body>') 
print('<h1>Fibonacci Sequence</h1>')
print('<a href="./fib.py?func=next">Next</a>')
print('<br>')

## Print the new numbers and the file
fileStr = ""
if lower:
    print('--- ')
    for i in range(2):
        print(str(numberList[i + 1]) + ' ')
else: 
    for num in numberList:
        print(str(num) + ' ')
if changed:
    for num in numberList:
        fileStr = fileStr + str(num) + ' '
    file = open("numbers.txt", "w")
    file.write(fileStr)

print('<br>')
if not lower:
    print('<a href="./fib.py?func=prev">Previous</a>')
print('</body>')
print('</html>')
