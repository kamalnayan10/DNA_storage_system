import random
from dnaValidator import DNAValidator
from utils import *

class DNAFountian():
    def __init__(self, validator = DNAValidator):
        self.file_path = None
        self.validator = validator()
        self.encoding = {"00":"A", "01": "C", "10":"G", "11":"T"}
        self.decoding = {"A": "00", "C": "01", "G":"10", "T":"11"}

        self.payload_len = 32
        self.seed_len = 4
        self.ecc_len = 2

        self.segments = []
        self.validated_dna = []

    def _segmentation(self):
        """
        Making 32 bytes segments of the input_file
        """

        byte_sequence = None
        with open(self.file_path, "rb") as f:
            byte_sequence = f.read()

        for i in range(0,len(byte_sequence), self.payload_len):
            segment = None
            if i+self.payload_len > len(byte_sequence):
                segment = byte_sequence[i:]
                padding_len = self.payload_len - len(segment)
                segment = segment + (b'\x00' * padding_len)
            else:
                segment = byte_sequence[i:i+self.payload_len]

            self.segments.append(segment)

    def _choose_degree(self):
        """
        Function to choose degree of a droplet where
        degree = number of segments the droplet is made up of
        """
        p = random.random()

        if p < 0.01:
            return 1
        elif p < 0.50:  
            return 2
        elif p < 0.67:
            return 3
        elif p < 0.77: 
            return 4
        else:
            return random.randint(5, 10)

    def _droplet_gen(self):
        """
        Function to develop one droplet using luby transform
        """

        seed = random.randint(0, 2**32 - 1)

        degree = self._choose_degree()

        random.seed(seed)

        if degree > len(self.segments):
            degree = len(self.segments)

        segment_indices = random.sample(range(len(self.segments)), degree)

        encoded_payload = b'\x00' * self.payload_len

        for index in segment_indices:
            segment = self.segments[index]
            encoded_payload = xor_bytes(encoded_payload, segment)

        seed_bytes = seed.to_bytes(self.seed_len, 'big')
        droplet = encoded_payload + seed_bytes # also need to add ecc here

        return droplet
    
    def encode(self, input_file_path):
        """
        Main function to create droplets, encode them and screen them
        and iterate over dorplet generation until we get proper encoding
        """

        self.file_path = input_file_path

        self._segmentation()

        num_droplets = int(len(self.segments) * 1.2)

        droplet_batch_size = int(num_droplets * 1.2)

        while len(self.validated_dna) < num_droplets:
            droplets_batch = [self._droplet_gen() for i in range(droplet_batch_size)]

            for droplet in droplets_batch:
                bit_string = "".join(f"{b:08b}" for b in droplet)
                dna_sequence = bit_to_dna(bit_string, self.encoding)

                if self.validator.validate_dna_sequence(dna_sequence):
                    self.validated_dna.append(dna_sequence)

            print(f"""
> Found {len(self.validated_dna)} / {num_droplets} valid sequences so far.
""")
            missing_count = num_droplets - len(self.validated_dna)

            if missing_count > 0:
                droplet_batch_size = int(missing_count * 1.20)
                # due to the 1.20 we might make more redundant codes,
                # which is fine

            
if __name__ == "__main__":
    dna = DNAFountian()

    dna.encode("sample.txt")
    print("NUMBER OF SEGMENTS")
    print(len(dna.segments))
    print("LENGTH OF DNA SAMPLES")
    print(len(dna.validated_dna))
