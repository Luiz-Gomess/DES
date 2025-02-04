from diffie_hellman import Diffie_Hellman
from des import DES
import socket

# Configuração do socket
host = 'localhost'
port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecta ao servidor
    sock.connect((host, port))
    print("Conectado ao servidor")

    print("------------------------------------------")

    print("Diffie-Hellman:")

    # cria uma instância da classe Diffie_Hellman
    receive = Diffie_Hellman(n=23, g=5)
    print("Chave privada do receive: ", receive.get_private_key())

    # gera a chave pública do receive
    receive.generate_public_key()
    public_key_receive = receive.get_public_key()
    print(f"Chave pública do receive: {public_key_receive}")

    # Envia a chave pública do receive
    sock.sendall(str(public_key_receive).encode('utf-8'))
    print("Chave pública do receive enviada")

    # Aguarda a chave pública do sender
    print("Aguardando chave pública do sender...")
    public_key_receive = sock.recvfrom(1024)
    print(f"Chave pública do sender: {public_key_receive[0].decode('utf-8')}")

    # Calcula o segredo compartilhado
    receive.calculate_shared_secret(int(public_key_receive[0].decode('utf-8')))
    shared_secret = receive.get_shared_secret()
    print(f"Segredo compartilhado: {shared_secret}")

    print("------------------------------------------")

    # cria uma instâcia da classe DES
    des = DES()
    print("Descriptografia:")

    # Aguarda a mensagem cifrada
    print("Aguardando mensagem cifrada...")
    ciphertext = sock.recvfrom(1024)[0]
    print(f"Mensagem cifrada recebida: {ciphertext.hex()}")

    # Descriptografa a mensagem
    plaintext = des.decrypt(ciphertext, str(shared_secret))
    print(f"Mensagem decifrada: {plaintext}")

finally:
    # Fecha a conexão
    sock.close()
    print("Conexão fechada")