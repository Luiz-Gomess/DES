INITIAL_PERMUTATION_TABLE = [

    58,	50,	42,	34,	26,	18,	10,	2,
    60,	52,	44,	36,	28,	20,	12,	4,
    62,	54,	46,	38,	30,	22,	14,	6,
    64,	56,	48,	40,	32,	24,	16,	8,
    57,	49,	41,	33,	25,	17,	9,  1,
    59,	51,	43,	35,	27,	19,	11,	3,
    61,	53,	45,	37,	29,	21,	13,	5,
    63,	55,	47,	39,	31,	23,	15,	7,
]

SHIFTS = [
    1,1,2,2,
    2,2,2,2,
    1,2,2,2,
    2,2,2,1
]

#Tabela de permutação de compreensão
COMP_PERMUTATION_TABLE = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

#Permutação Inicial
def block_permutation(block):
    """Permutação Inicial

        Reposiciona os bits com base nos valores da tabela.
    Args:
        block (str): bloco de bits

    Returns:
        str: bloco de bits reposicionados
    """
    permuted_block = ''
    for position in INITIAL_PERMUTATION_TABLE:
        permuted_block += block[position-1]
    
    return permuted_block

#Separa o resultado da permutação inicial em duas variaveis de 32 bits cada.
def spliting_halves(permuted_block):
    left = ''
    right = ''

    for index, bit in enumerate(permuted_block):
        if index < len(permuted_block) //2:
            left += bit
        else:
            right += bit
    
    return left, right

#Gerador da chave original
def key_generation(key):
    """Gera uma chave original de 56 bits.
    A chave bruta é recebida com o tamanho de 64 bits e reduzida para 56 bits,
    descartando seus bits múltiplos de 8. 

    Args:
        key (str): chave bruta de 64 bits. 

    Returns:
        str: chave de 56 bits
    """
    key_56bits = ''

    for position, bit in enumerate(key):
        if position in [x for x in range(7,64,8)]:
            pass
        else:
            key_56bits += bit
    
    return key_56bits

#Rotações a esquerda
def shifts_left(half_key, shifts):
    """Rotaciona os bits a esquerda conforme o numero de
      saltos recebido.

    Args:
        half_key (str): Metade da chave de 56 bits.
        shifts (int): Numero de saltos a esquerda. 

    Returns:
        str: Parte da chave rotacionada a esquerda
    """
    rotated_key = ''
    for _ in range(shifts):
        for i in range(1, len(half_key)):
            rotated_key += half_key[i]
        rotated_key += half_key[0]
        half_key = rotated_key
        rotated_key = ''

    return half_key

#Gerador de sub-chaves
def compression_permutation(string56bit):
    """
    Gera uma sub-chave de 48 bits proveniente da 
    chave original de 56 bits.

    Args:
        string56bit (_type_): _description_

    Returns:
        _type_: _description_
    """
    comp_permutation = ''

    for i in range(0, 48):
        comp_permutation += string56bit[COMP_PERMUTATION_TABLE[i]-1]

    return comp_permutation


if __name__ == "__main__":

    entry = "ifpbifpb"
    block = ''.join(format(ord(i), '08b') for i in entry)

    key = 'ifpbifpb'
    bin_key = ''.join(format(ord(i), '08b') for i in key)

    permuted_block = block_permutation(block)
    left, right = spliting_halves(permuted_block)

    generated_56bit_key = key_generation(bin_key)


    # print(left)
    # print(right)

    # print(permuted_block == left + right)
    print(block)
    print(len(generated_56bit_key))

    len(left)

    left
    shifts_left(left, 1)
    

    right








# permuted_text = bitarray(bitarray(res)[x - 1] for x in INITIAL_PERMUTATION_TABLE)


