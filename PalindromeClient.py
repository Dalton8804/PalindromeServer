from socket import *
from os.path import exists

serverAddress = ('127.0.0.1', 8888)
clients = []
files = []
fileNames = []
numOfClients = input("How many clients would you like to process? ")
numOfClients = int(numOfClients)

for index in range(0, numOfClients):
    clients.append(socket(AF_INET, SOCK_STREAM))

for index in range(0, numOfClients):
    print("Enter the file name for client " + str(index + 1) + ": (i.e. client1.dat)")
    while True:
        filepath = input()
        if exists(filepath):
            fileNames.append(filepath)
            files.append(open(fileNames[index], "r"))
            break
        else:
            print("Make sure you typed the file name in correctly, try again. ")
nameIndex = 0
for file in files:
    index = 0
    counter = 1
    for line in file:
        for client in clients:
            if index == clients.index(client):  # sorry this is such a hacky way to do this, my other methods were failing :(
                try:
                    client.connect(serverAddress)
                except:
                    pass
                line = line.rstrip('\n')
                client.send(line.encode())
                data = client.recv(1024)
                print("Line " + str(counter) + " in " + fileNames[nameIndex] + ": " + line + ": " + str(data)[2:-1])
                counter += 1
    index += 1
    nameIndex += 1
