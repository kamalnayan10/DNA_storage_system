class DNA_System():
    def __init__(self):
        self.encoding = {"00":"A", "01": "C", "10":"G", "11":"T"} # Church Method Encoding
        self.decoding = {"A": "00", "C": "01", "G":"10", "T":"11"} # Church Method Decoding
    
    def _homopolymer_check(self, dna_sequence, max_allowed = 3):
        validity = True

        if len(dna_sequence) <= max_allowed:
            return True

        same_count = 1
        prev_hp = dna_sequence[0]

        for i in range(1,len(dna_sequence)):

            if dna_sequence[i] == prev_hp:
                same_count += 1
            else:
                same_count = 1

            if same_count > max_allowed:
                validity = False
                break

            prev_hp = dna_sequence[i]
            
        return validity
    

    def _gc_content_check(self, dna_sequence, acceptable_range = (0.4,0.6)):
        if not dna_sequence:
            return True

        gc_count = dna_sequence.count('G') + dna_sequence.count('C')

        gc_ratio = gc_count/len(dna_sequence)

        return acceptable_range[0] <= gc_ratio <= acceptable_range[1]
    
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
    
    def validate_dna_sequence(self, dna_sequence):

        homopolymer_validity = self._homopolymer_check(dna_sequence)
        gc_content_validity = self._gc_content_check(dna_sequence)

        if homopolymer_validity and gc_content_validity:
            return True
        
        else:
            if not homopolymer_validity:
                print("Homopolymer chain greater than 3")
            if not gc_content_validity:
                print("GC content not in the ideal range")

        return False


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

    print("DNA Sequence validity", "valid" if dna.validate_dna_sequence(dna_seq) else "invalid")

    dna.dna_to_text_file(dna_seq)