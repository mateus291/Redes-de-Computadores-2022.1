from socket import socket, AF_INET, SOCK_STREAM

command_list = ['USER', 'RETR', 'QUIT']

HOST = '127.0.0.1'
PORT = 12000

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))

while True:
    sock.listen()

    conn, addr = sock.accept()
    print("Connected to " , addr)

    remainder = ''

    while True:
        command = ''

        if remainder == '':
            # Se não há comandos esperando por execução, receba novos:
            data = conn.recv(1024).decode('utf-8')
            command = data.split(' ')[0].upper()
        else:
            # Se ainda há comandos esperando, execute-os:
            data = remainder
            space = remainder.find(' ')
            command = remainder[:space].upper()
            remainder = ''
        
        if command in command_list:
            if command == "QUIT":
                conn.send('221 Goodbye.\r\n'.encode('utf-8'))
                break
            
            if command == 'USER':
                conn.send('331 OK.\r\n'.encode('utf-8'))

            if command == "RETR":
                filename = data.split(' ')[1]
                try: 
                    with open(filename, 'rb') as f:
                        conn.send('150 Opening data connection.\r\n'.encode('utf-8'))
                        datasock = socket(AF_INET, SOCK_STREAM)
                        datasock.connect((HOST, PORT + 21))
                        f_data = f.read(1024)
                        
                        while data:
                            datasock.send(f_data)
                            f_data = f.read(1024)
                        
                        datasock.close()
                        conn.send('226 Transfer complete.\r\n'.encode('utf-8'))
                except:
                    conn.send('501 Syntax error in paramenters or arguments.\r\n'.encode('utf-8'))
        

    # If loop exitted, have disconnected
    print("Disconnected from:", addr)

# close the server   
sock.close()
