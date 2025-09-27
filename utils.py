def xor_bytes(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])

def bit_to_dna(bit_string, encoding):
    dna_sequence = ""

    for i in range(0,len(bit_string), 2):
        dna_sequence += encoding[bit_string[i:i+2]]

    return dna_sequence