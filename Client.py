import socket
import threading

# Configurações do cliente
HOST = '10.11.12.125'  # Endereço IP do servidor
PORT = 12345       # Porta do servidor

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
    except Exception as e:
        print(f"Erro na conexão com o servidor: {str(e)}")

# Função principal do cliente
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Solicita o nome do cliente
    client_name = input("Digite seu nome: ")
    client_socket.send(client_name.encode('utf-8'))

    # Inicia uma thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input()
            client_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Cliente encerrado")

if __name__ == "__main__":
    main()
