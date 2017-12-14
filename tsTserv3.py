"""
Henry Ang
2/7/17
CSC 4800
Chapter 2: TCP Server/Client
TCP Server: recognize the following commands:

EXITSERVER - recieves "EXITSERVER" message. Close client, server socket. Terminate client connection.
date - receives "date" message. Returns current date/time stamp
os - receives "os" message. Returns os information
ls (serverpath) - receives "ls (serverpath)" message. Returns current or specified directory
sleep (secs) - receives "sleep (secs)" message. Returns sleep seconds and server sleeps for specified seconds.
"""

from socket import *
from time import *
import sys, os, re

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

# server recognized messages
EXIT_MESSAGE = "EXITSERVER"
DATE_MESSAGE = "date"
OS_MESSAGE = "os"
PATH_MESSAGE= "ls"
SLEEP_MESSAGE = "sleep"

while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:               # check is no data inputted
            break
        recievedData = str(data.decode('utf-8'))

        sleepNumMatch = re.match("(sleep)[ ](\d+)", recievedData)      # match for valid sleep sec
        lsMatch = re.match("^(ls)[ ]([\d+\w+/.-_ ]+)$", recievedData) # match of valid ls server-path

        if recievedData == EXIT_MESSAGE:                  # if data recieved from client is "EXITSERVER"
            tcpCliSock.shutdown(1)                        # shutdown client socket
            tcpCliSock.close()                            # close client socket
            tcpSerSock.close()                            # close server socket
            sys.exit()                                    # terminate server

        elif recievedData == DATE_MESSAGE:                 # if data recieved from client is "date"
            tcpCliSock.send(bytes(ctime(), 'utf-8'))

        elif recievedData == OS_MESSAGE:                   # if data recieved from client is "os"
            tcpCliSock.send(bytes(os.name, 'utf-8'))

        elif recievedData == PATH_MESSAGE:                  # if data recieved from client is "ls"
            tcpCliSock.send(bytes('%s' % (os.listdir()), 'utf-8'))

        elif lsMatch != None:                               # if data recieved from client is valid directory
            try:
                other, lsFinal = lsMatch.groups()
                tcpCliSock.send(bytes('%s' % (os.listdir(lsFinal)), 'utf-8'))
            except FileNotFoundError:
                tcpCliSock.send(bytes("Directory not found", 'utf-8'))
            except Exception:
                tcpCliSock.send(bytes("Cannot access Directory", 'utf-8'))

        elif recievedData == SLEEP_MESSAGE:                 # if data recieved from client is "sleep"
            sleep(5)                                        # sleeps for 5 seconds
            tcpCliSock.send(bytes('%s' % (5), 'utf-8'))

        elif sleepNumMatch != None:                         # if data recieved from client is valid sleep
            other, sleepFinal = sleepNumMatch.groups()
            sleep(int(sleepFinal))                          # sleep for specified time
            tcpCliSock.send(bytes('%s' % (sleepFinal), 'utf-8'))

        else:                                               # default behavior
            tcpCliSock.send(bytes('[%s] %s' % (ctime(), data.decode('utf-8')), 'utf-8'))

    tcpCliSock.close()
tcpSerSock.close()
