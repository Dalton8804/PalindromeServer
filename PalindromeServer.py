import sys
from socket import *
import select
import queue


def isPalindrome(s):
    if s == s[::-1]:
        return 'Yes'
    return 'No'


serverPort = 12
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Ready to receive...')

inputs = [serverSocket]
outputs = []
messages_Queue = {}

while True:
    readable, writable, exceptional = select.select(inputs, outputs, [])
    for s in readable:
        if s is serverSocket:
            clientSocket, addr = s.accept()
            print('Ready to serve...')
            inputs.append(clientSocket)
            messages_Queue[clientSocket] = queue.Queue()
            line = clientSocket.recv(1024)
            clientSocket.send(isPalindrome(line).encode())
        else:
            data = s.recv(1024)
            if data:
                # A readable client socket has data
                messages_Queue[s].put(isPalindrome(data).encode())
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del messages_Queue[s]

    for s in writable:
        try:
            next_msg = messages_Queue[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)
    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        del messages_Queue[s]

