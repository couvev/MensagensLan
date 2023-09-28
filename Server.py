import socket
import threading

# Configurações do servidor
HOST = '10.11.12.125'  # Endereço IP do servidor
PORT = 12345       # Porta para conexão

# Dicionário para armazenar os clientes conectados e seus respectivos sockets
clientes = {}

# Função para lidar com as mensagens recebidas de um cliente
def handle_client(client_socket, client_address):
    try:
        # Recebe o nome do cliente
        client_name = client_socket.recv(1024).decode('utf-8')
        print(f"Conexão estabelecida com {client_name} ({client_address[0]}:{client_address[1]})")

        # Adiciona o cliente à lista de clientes
        clientes[client_name] = client_socket

        # Aguarda mensagens do cliente e encaminha para outros clientes
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{client_name}: {message}")
            broadcast_message(client_name, message)

    except Exception as e:
        print(f"Erro na conexão com {client_name}: {str(e)}")
    finally:
        # Remove o cliente da lista quando a conexão é encerrada
        del clientes[client_name]
        client_socket.close()
        print(f"{client_name} desconectado")

# Função para enviar mensagens para todos os clientes
def broadcast_message(sender, message):
    for client_name, client_socket in clientes.items():
        if client_name != sender:
            try:
                client_socket.send(f"{sender}: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Erro ao enviar mensagem para {client_name}: {str(e)}")

# Função principal do servidor
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor escutando em {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Servidor encerrado")

if __name__ == "__main__":
    main()
