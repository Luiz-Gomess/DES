

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


entry = "ifpbifpb"
block = ''.join(format(ord(i), '08b') for i in entry)



def block_permutation(block):
    permuted_block = ''
    for position in INITIAL_PERMUTATION_TABLE:
        permuted_block += block[position-1]
    
    return permuted_block

def spliting_halves(permuted_block):
    left = ''
    right = ''

    for index, bit in enumerate(permuted_block):
        if index < len(permuted_block) //2:
            left += bit
        else:
            right += bit
    
    return left, right


if __name__ == "__main__":

    entry = "ifpbifpb"
    block = ''.join(format(ord(i), '08b') for i in entry)

    permuted_block = block_permutation(block)
    left, right = spliting_halves(permuted_block)

    print(left)
    print(right)

    print(permuted_block == left + right)
 










# permuted_text = bitarray(bitarray(res)[x - 1] for x in INITIAL_PERMUTATION_TABLE)


