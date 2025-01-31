from tabelas import PERMUTACAO_INICIAL, PERMUTACAO_FINAL, PERMUTACAO, PC1, PC2, S_BOXES, SHIFTS, EXPANSAO_T

class DES:
    PI = PERMUTACAO_INICIAL
    PF = PERMUTACAO_FINAL
    P = PERMUTACAO
    PC1 = PC1
    PC2 = PC2
    S_BOXES = S_BOXES
    SHIFTS = SHIFTS
    E = EXPANSAO_T

    def __init__(self):
        pass

    #Funções auxiliares
    def __permute(self, bits, table):
        """ Aplica permutação usando uma tabela """
        return [bits[i-1] for i in table]

    def __left_shift(self, bits, n):
        """ Deslocamento circular para esquerda """
        return bits[n:] + bits[:n]

    def __xor(self, bits1, bits2):
        """ XOR entre duas listas de bits """
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]
    
    def __adjust_key(self, key):
        """Ajusta a chave para 64 bits (8 bytes)"""
        key_bytes = key.encode('utf-8')[:8]  # Trunca para 8 bytes
        if len(key_bytes) < 8:
            key_bytes += b'\x00' * (8 - len(key_bytes))  # Padding com zeros
        return key_bytes

    def __pad_message(self, message):
        """Preenche a mensagem usando PKCS#7"""
        pad_len = 8 - (len(message) % 8)
        return message + bytes([pad_len] * pad_len)

    def __unpad_message(self, padded):
        """Remove padding PKCS#7"""
        pad_len = padded[-1]
        return padded[:-pad_len]
    
    #Funções do DES

    def generate_subkeys(self, key_bits):
        """ Gera as 16 subchaves para o DES """
        # Permutação PC-1
        key = self.__permute(key_bits, self.PC1)

        # Divide em C0 e D0
        C = key[:28]
        D = key[28:]

        subkeys = []
        for shift in self.SHIFTS:
            # Desloca as metades
            C = self.__left_shift(C, shift)
            D = self.__left_shift(D, shift)

            # Combina e aplica PC-2
            combined = C + D
            subkey = self.__permute(combined, self.PC2)
            subkeys.append(subkey)

        return subkeys
    
    def __encrypt_block(self, block_bits: list[int], subkeys: list[int]):
        """Cifra um bloco de 64 bits

        Args:
            block_bits (list[int]): Bloco a ser cifrado
            subkeys (list[int]): Lista de subchaves geradas

        Returns:
            _type_: _description_
        """
        # Permutação inicial
        block = self.__permute(block_bits, PERMUTACAO_INICIAL)
        
        L = block[:32]
        R = block[32:]
        
        # 16 rodadas de Feistel
        for i in range(16):
            # Expansão
            R_expanded = self.__permute(R, self.E)
            
            # XOR com subkey
            mixed = self.__xor(R_expanded, subkeys[i])
            
            # Substituição S-Box
            substituted = []
            for j in range(8):
                chunk = mixed[j*6:(j+1)*6]
                row = (chunk[0] << 1) + chunk[5]
                col = (chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4]
                val = S_BOXES[j][row][col]
                substituted += [int(b) for b in f"{val:04b}"]
            
            # Permutação PERMUTACAO
            permuted = self.__permute(substituted, self.P)
            
            # XOR com L
            new_R = self.__xor(L, permuted)
            
            # Atualiza L e R
            L = R
            R = new_R
        
        # Combinação final
        combined = R + L
        
        # Permutação final
        ciphertext = self.__permute(combined, PERMUTACAO_FINAL)

        return ciphertext
    

    def __decrypt_block(self, block_bits, subkeys):
        """
        Decifra um bloco de 64 bits usando as subchaves 
        em ordem inversa
        """
        return self.__encrypt_block(block_bits, subkeys[::-1])
    
    
    def encrypt(self, plaintext: str, key: str) -> bytes:
        """Cifra a mensagem recebida

        Args:
            plaintext (str): Texto a ser cifrado
            key (str): Chave 

        Returns:
            bytes: Texto cifrado em bytes
        """
        key_bytes = self.__adjust_key(key)
        key_bits = [int(bit) for byte in key_bytes for bit in f"{byte:08b}"]
        subkeys = self.generate_subkeys(key_bits)
        
        padded = self.__pad_message(plaintext.encode('utf-8'))
        ciphertext = b''
        
        for i in range(0, len(padded), 8):
            block = padded[i:i+8]
            block_bits = [int(bit) for byte in block for bit in f"{byte:08b}"]
            encrypted_bits = self.__encrypt_block(block_bits, subkeys)
            
            # Converte os bits cifrados de volta para bytes
            encrypted_bytes = bytes(
                int(''.join(map(str, encrypted_bits[i:i+8])), 2)
                for i in range(0, 64, 8)
            )
            ciphertext += encrypted_bytes
        
        return ciphertext
    
    
    def decrypt(self, ciphertext: bytes, key: str) -> str:
        """Descriptografa a mensagem cifrada.

        Args:
            ciphertext (bytes): Texto cifrado em bytes.
            key (str): Chave utilizada para a cifragem do texto.

        Returns:
            str: Mensagem descriptografada.
        """

        key_bytes = self.__adjust_key(key)
        key_bits = [int(bit) for byte in key_bytes for bit in f"{byte:08b}"]
        subkeys = self.generate_subkeys(key_bits)
        
        padded_message = b''
        
        # Processa cada bloco de 64 bits (8 bytes)
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            block_bits = [int(bit) for byte in block for bit in f"{byte:08b}"]
            
            # Decifra o bloco com as subchaves em ordem inversa
            decrypted_bits = self.__decrypt_block(block_bits, subkeys)
            
            # Converte os bits decifrados para bytes
            decrypted_bytes = bytes(
                int(''.join(map(str, decrypted_bits[i:i+8])), 2)
                for i in range(0, 64, 8)
            )
            padded_message += decrypted_bytes
        
        # Remove o padding e retorna o texto original
        return self.__unpad_message(padded_message).decode('utf-8')
            

    def main(self, key:str, plaintext:str):
        print("Criptografia:")
        ciphertext = self.encrypt(plaintext, key)
        print(f"Texto original: {plaintext}")
        print(f"Texto cifrado (hex): {ciphertext.hex()}")

        print("\nDescriptografia:")
        decrypted_text = self.decrypt(ciphertext, key)
        print(f"Texto decifrado: {decrypted_text}")

        print("\nResultado:", "Sucesso!" if decrypted_text == plaintext else "Falha!")


if __name__ == "__main__":
    
    chave = "5"
    plaintext = "THIS IS A LITTLE TEXT TO CIPHER"

    des = DES()
    des.main(key=chave, plaintext= plaintext)


