


class DNA_System():
    def __init__(self):
        self.encoding = {"00":"A", "01": "C", "10":"G", "11":"T"} # Church Method Encoding
        self.decoding = {"A": "00", "C": "01", "G":"10", "T":"11"} # Church Method Decoding

    def text_file_to_dna(self, text_file):
        byte_sequence = None
        with open(text_file, "rb") as f:
            byte_sequence = f.read()

        bit_sequence = "".join(f"{b:08b}" for b in byte_sequence)

        dna_sequence = ""
        for i in range(0, len(bit_sequence) ,2):
            dna_sequence += self.encoding[bit_sequence[i:i+2]]

        f.close()
        
        return dna_sequence

    
    def dna_to_text_file(self, dna_sequence):
        bit_sequence = ""
        
        for i in range(len(dna_sequence)):
            bit_sequence += self.decoding[dna_sequence[i]]
        
        byte_sequence = []

        for i in range(0, len(bit_sequence), 8):
            byte_sequence.append(int(bit_sequence[i:i+8], 2))

        with open("sample_decoded.txt", "wb") as f:
            f.write(bytes(byte_sequence))

        f.close()


if __name__ == "__main__":
    dna = DNA_System()

    dna_seq = dna.text_file_to_dna("sample.txt")

    print("Corresponding DNA Sequence: ", dna_seq)

    dna.dna_to_text_file(dna_seq)