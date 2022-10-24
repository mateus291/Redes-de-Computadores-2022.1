# -*- coding: utf-8 -*-

import socket as sk

serverPort = 12000
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM) 
serverSocket.bind(('', serverPort)) 
serverSocket.listen(10)

print('Servidor pronto para receber!')

while 1:
    connectionSocket, addr = serverSocket.accept()
    
    request = connectionSocket.recv(1024).decode('utf-8')
    headers = request.split('\n')
    filename = headers[0].split()[1]

    try:
        file = open('documents/' + filename)
        data = bytes(file.read(), 'utf-8')

        connectionSocket.send(b'File located')
        connectionSocket.send(data)

    except IOError:
        connectionSocket.send(b'404 Not Found')
    
    connectionSocket.close()
    