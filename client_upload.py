import socket
import os
import struct

# Configurações do cliente
SERVER_IP = '127.0.0.1'  # Troque pelo IP real do servidor
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def send_file(filename):
    if not os.path.exists(filename):
        print(f"Erro: Arquivo {filename} não existe.")
        return

    # Cria o socket do cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Conectado ao servidor {SERVER_IP}:{SERVER_PORT}.")

        # Envia o nome do arquivo
        filename_bytes = filename.encode('utf-8')
        client_socket.sendall(struct.pack('I', len(filename_bytes)))
        client_socket.sendall(filename_bytes)

        # Envia o conteúdo do arquivo
        with open(filename, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                client_socket.sendall(data)

        print(f"Arquivo {filename} enviado com sucesso.")

if __name__ == '__main__':
    filename = input("Digite o nome do arquivo para enviar: ")
    send_file(filename)
