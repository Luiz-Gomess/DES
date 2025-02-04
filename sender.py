from des import DES
from diffie_hellman import Diffie_Hellman
import socket

# Configuração do socket
host = 'localhost'
port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula o socket ao endereço e porta
sock.bind((host, port))

# Escuta por conexões
sock.listen(1)
print("Aguardando conexão...")

# Aceita a conexão de um cliente
conn, addr = sock.accept()
print(f"Conectado ao cliente: {addr}")

try:
    print("------------------------------------------")

    print("Diffie-Hellman:")

    # cria uma instância da classe Diffie_Hellman
    
    sender = Diffie_Hellman(n=23, g=5)
    print("Chave privada do sender: ", sender.get_private_key())

    # gera a chave pública do sender
    sender.generate_public_key()
    public_key_sender = sender.get_public_key()
    print(f"Chave pública do sender: {public_key_sender}")

    # Envia a chave pública do sender
    conn.sendall(str(public_key_sender).encode('utf-8'))
    print("Chave pública do sender enviada")

    # Aguarda a chave pública do receiver
    print("Aguardando chave pública do receiver...")
    public_key_receive = conn.recv(1024)
    print(f"Chave pública do receiver: {public_key_receive.decode('utf-8')}")

    # Calcula o segredo compartilhado
    sender.calculate_shared_secret(int(public_key_receive.decode('utf-8')))
    shared_secret = sender.get_shared_secret()
    print(f"Segredo compartilhado: {shared_secret}")

    print("------------------------------------------")

    # cria uma instância da classe DES
    des = DES()
    print("Criptografia:")
    plaintext = input("Digite a mensagem a ser cifrada: ")

    # Cifra a mensagem
    ciphertext = des.encrypt(plaintext, str(shared_secret))
    print(f"Mensagem cifrada: {ciphertext.hex()}")

    # Envia a mensagem cifrada
    conn.sendall(ciphertext)
    print("Mensagem cifrada enviada")

finally:
    # Fecha a conexão
    conn.close()
    print("Conexão fechada")