import random


class Diffie_Hellman:
    def __init__(self, n: int, g: int):
        self.n = n
        self.g = g
        self.private_key = random.randint(2, 100)
        self.public_key = None
        self.shared_secret = None

    def resolve_key(self, key_value: int) -> int:
        """Resolve a chave pública ou compartilhada.
        
        Args: key_value (int): valor da chave para efetuar o calculo.

        Returns: int: valor da chave resolvida.
        
        """
        return (key_value ** self.private_key) % self.n

    def generate_public_key(self):
        """Gera a chave pública, utilizando a fórmula do metodo resolve_key."""
        
        self.public_key = self.resolve_key(self.g)

    def get_public_key(self) -> int:
        """Retorna a chave pública.
        
        returns: int: chave pública.
        """
        return self.public_key
    
    def calculate_shared_secret(self, received_public_key: int):
        """Calcula o segredo compartilhada, utilizando a chave pública recebida.
        
        Args: received_public_key (int): chave pública recebida.
        """
        self.shared_secret = self.resolve_key(received_public_key)

    def get_shared_secret(self) -> int:
        """Retorna o segredo compartilhado.
        
        Returns: int: segredo compartilhado.
        """
        return self.shared_secret
    
if __name__ == "__main__":
    n = 23
    g = 5
    alice = Diffie_Hellman(n, g)
    bob = Diffie_Hellman(n, g)

    alice.generate_public_key()
    bob.generate_public_key()

    alice.calculate_shared_secret(bob.get_public_key())
    bob.calculate_shared_secret(alice.get_public_key())

    print("Alice:", alice.get_shared_secret())
    print("Bob:", bob.get_shared_secret())