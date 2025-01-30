import struct

# ==============================================
# TABELAS OFICIAIS DO DES (FIPS PUB 46-3)
# ==============================================

# Permutação Inicial (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Permutação Final (IP⁻¹)
IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Expansão (E)
E = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

# Permutação (P)
P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# S-Boxes
S_BOX = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Tabelas de permutação de chaves
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Número de rotações por rodada
SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

# ==============================================
# FUNÇÕES AUXILIARES
# ==============================================

def text_to_bits(text):
    """Converte texto para lista de bits"""
    return [int(bit) for byte in text.encode('utf-8') for bit in f"{byte:08b}"]

def bits_to_text(bits):
    """Converte lista de bits para texto"""
    bytes_list = [int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]
    return bytes(bytes_list).decode('utf-8', errors='replace')

def hex_to_bits(hex_str):
    """Converte hexadecimal para lista de bits"""
    return [int(bit) for byte in bytes.fromhex(hex_str) for bit in f"{byte:08b}"]

def bits_to_hex(bits):
    """Converte lista de bits para hexadecimal"""
    bytes_list = bytes([int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)])
    return bytes_list.hex()

def permute(bits, table):
    """Aplica permutação usando uma tabela"""
    return [bits[i-1] for i in table]

def left_shift(bits, n):
    """Deslocamento circular para esquerda"""
    return bits[n:] + bits[:n]

def xor(bits1, bits2):
    """XOR entre duas listas de bits"""
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

# ==============================================
# FUNÇÕES PRINCIPAIS DO DES
# ==============================================

def generate_subkeys(key_bits):
    """Gera as 16 subchaves para o DES"""
    # Permutação PC-1
    key = permute(key_bits, PC1)
    
    # Divide em C0 e D0
    C = key[:28]
    D = key[28:]
    
    subkeys = []
    for shift in SHIFT_SCHEDULE:
        # Desloca as metades
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        
        # Combina e aplica PC-2
        combined = C + D
        subkey = permute(combined, PC2)
        subkeys.append(subkey)
    
    return subkeys

def des_encrypt_block(block_bits, subkeys):
    """Cifra um bloco de 64 bits usando DES"""
    # Permutação inicial
    block = permute(block_bits, IP)
    
    L = block[:32]
    R = block[32:]
    
    # 16 rodadas de Feistel
    for i in range(16):
        # Expansão
        R_expanded = permute(R, E)
        
        # XOR com subkey
        mixed = xor(R_expanded, subkeys[i])
        
        # Substituição S-Box
        substituted = []
        for j in range(8):
            chunk = mixed[j*6:(j+1)*6]
            row = (chunk[0] << 1) + chunk[5]
            col = (chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4]
            val = S_BOX[j][row][col]
            substituted += [int(b) for b in f"{val:04b}"]
        
        # Permutação P
        permuted = permute(substituted, P)
        
        # XOR com L
        new_R = xor(L, permuted)
        
        # Atualiza L e R
        L = R
        R = new_R
    
    # Combinação final
    combined = R + L
    
    # Permutação final
    ciphertext = permute(combined, IP_INV)
    return ciphertext

def des_decrypt(ciphertext, key):
    """Decifra uma mensagem completa usando DES"""
    key_bytes = adjust_key(key)
    key_bits = [int(bit) for byte in key_bytes for bit in f"{byte:08b}"]
    subkeys = generate_subkeys(key_bits)
    
    padded_message = b''
    
    # Processa cada bloco de 64 bits (8 bytes)
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        block_bits = [int(bit) for byte in block for bit in f"{byte:08b}"]
        
        # Decifra o bloco com as subchaves em ordem inversa
        decrypted_bits = des_decrypt_block(block_bits, subkeys)
        
        # Converte os bits decifrados para bytes
        decrypted_bytes = bytes(
            int(''.join(map(str, decrypted_bits[i:i+8])), 2)
            for i in range(0, 64, 8)
        )
        padded_message += decrypted_bytes
    
    # Remove o padding e retorna o texto original
    return unpad_message(padded_message).decode('utf-8')

def des_decrypt_block(block_bits, subkeys):
    """Decifra um bloco de 64 bits usando DES"""
    # Usa as subchaves em ordem inversa
    return des_encrypt_block(block_bits, subkeys[::-1])

# ==============================================
# FUNÇÕES DE ALTO NÍVEL
# ==============================================

def adjust_key(key):
    """Ajusta a chave para 64 bits (8 bytes)"""
    key_bytes = key.encode('utf-8')[:8]  # Trunca para 8 bytes
    if len(key_bytes) < 8:
        key_bytes += b'\x00' * (8 - len(key_bytes))  # Padding com zeros
    return key_bytes

def pad_message(message):
    """Preenche a mensagem usando PKCS#7"""
    pad_len = 8 - (len(message) % 8)
    return message + bytes([pad_len] * pad_len)

def unpad_message(padded):
    """Remove padding PKCS#7"""
    pad_len = padded[-1]
    return padded[:-pad_len]

def des_encrypt(plaintext, key):
    """Cifra uma mensagem completa usando DES"""
    key_bytes = adjust_key(key)
    key_bits = [int(bit) for byte in key_bytes for bit in f"{byte:08b}"]
    subkeys = generate_subkeys(key_bits)
    
    padded = pad_message(plaintext.encode('utf-8'))
    ciphertext = b''
    
    for i in range(0, len(padded), 8):
        block = padded[i:i+8]
        block_bits = [int(bit) for byte in block for bit in f"{byte:08b}"]
        encrypted_bits = des_encrypt_block(block_bits, subkeys)
        
        # Converte os bits cifrados de volta para bytes
        encrypted_bytes = bytes(
            int(''.join(map(str, encrypted_bits[i:i+8])), 2)
            for i in range(0, 64, 8)
        )
        ciphertext += encrypted_bytes
    
    return ciphertext

# Funções DES implementadas anteriormente devem estar no código

# ============= CONFIGURAÇÃO =============
key = "mysecretkey"
plaintext = "Hell"

# ============= ETAPAS =============
print("Passo 1 - Ajuste da chave para 64 bits:")
adjusted_key = adjust_key(key)
print(f"Chave original: {key}")
print(f"Chave ajustada: {adjusted_key} (hex: {adjusted_key.hex()})")

print("\nPasso 2 - Criptografia:")
ciphertext = des_encrypt(plaintext, key)
print(f"Texto original: {plaintext}")
print(f"Texto cifrado (hex): {ciphertext.hex()}")

print("\nPasso 3 - Descriptografia:")
decrypted_text = des_decrypt(ciphertext, key)
print(f"Texto decifrado: {decrypted_text}")

# ============= VERIFICAÇÃO =============
print("\nResultado:", "Sucesso!" if decrypted_text == plaintext else "Falha!")