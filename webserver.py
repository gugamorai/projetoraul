# webserver.py
from socket import *
import sys  # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverPort = 6789
serverSocket.bind(('', serverPort))   # '' = todas as interfaces locais
serverSocket.listen(1)                # Habilita a aceitar conexões

print(f"Servidor rodando na porta {serverPort}. Ctrl+C para parar.")

while True:
    try:
        # Estabelece conexão
        connectionSocket, addr = serverSocket.accept()
        
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()

        if not message:
            connectionSocket.close()
            continue

        # Extrai o nome do arquivo pedido
        filename = message.split()[1]

        # Remove a barra inicial "/"
        filename = filename[1:]

        # Abre o arquivo solicitado
        f = open(filename)
        outputdata = f.read()

        # Envia cabeçalho HTTP
        header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(header.encode())

        # Envia conteúdo do arquivo
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())

        # Fecha conexão
        connectionSocket.close()

    except IOError:
        # Se não encontrar o arquivo, envia erro 404
        header = "HTTP/1.1 404 Not Found\r\n\r\n"
        connectionSocket.send(header.encode())
        connectionSocket.send("<h1>404 Not Found</h1>".encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()
