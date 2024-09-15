import socket
import os
import uuid
import psutil
import struct

# Função para obter o endereço MAC da interface conectada à internet
def get_mac_address():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                return addr.address
    return None

# Função para gerar UUID baseado no MAC address
def generate_uuid_from_mac():
    mac_address = get_mac_address()
    if mac_address:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, mac_address))
    return None

# Configurações do servidor
SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def start_server():
    # Gera UUID baseado no MAC address do servidor
    server_uuid = generate_uuid_from_mac()
    if not server_uuid:
        print("Falha ao obter o endereço MAC.")
        return
    print(f"UUID do servidor: {server_uuid}")

    # Cria o socket do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(5)
        print(f"Servidor ouvindo em {SERVER_IP}:{SERVER_PORT}...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Cliente conectado: {client_address}")

            # Recebe o nome do arquivo
            filename_size = struct.unpack('I', client_socket.recv(4))[0]
            filename = client_socket.recv(filename_size).decode('utf-8')
            print(f"Recebendo arquivo: {filename}")

            # Cria o arquivo de destino
            with open(filename, 'wb') as f:
                while True:
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
            print(f"Arquivo {filename} recebido com sucesso.")

            client_socket.close()

if __name__ == '__main__':
    start_server()
