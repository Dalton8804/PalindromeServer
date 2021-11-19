from socket import *

serverAddress = ('', 12)
socks = [socket(AF_INET, SOCK_STREAM), socket(AF_INET, SOCK_STREAM)]
for s in socks:
    s.connect(serverAddress)
f = open('Client1.txt', 'r')
for line in f:
    line=line.rstrip('\n')
    for s in socks:
        s.send(line.encode())
    for s in socks:
        data = s.recv(1024)
        print(line+": "+str(data)[2:-1])

