class DNAValidator():
    
    def __init__(self, hp_max = 3, gc_range = (0.4,0.6)):
        self.hp_max = hp_max
        self.gc_range = gc_range

    def _homopolymer_check(self, dna_sequence):
        validity = True

        if len(dna_sequence) <= self.hp_max :
            return True

        same_count = 1
        prev_hp = dna_sequence[0]

        for i in range(1,len(dna_sequence)):

            if dna_sequence[i] == prev_hp:
                same_count += 1
            else:
                same_count = 1

            if same_count > self.hp_max :
                validity = False
                break

            prev_hp = dna_sequence[i]
            
        return validity
    

    def _gc_content_check(self, dna_sequence):
        if not dna_sequence:
            return True

        gc_count = dna_sequence.count('G') + dna_sequence.count('C')

        gc_ratio = gc_count/len(dna_sequence)

        return self.gc_range[0] <= gc_ratio <= self.gc_range[1]
    
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
