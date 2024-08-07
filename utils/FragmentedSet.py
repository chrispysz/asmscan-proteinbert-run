import os
from typing import List, Tuple

from utils.datasets import load_fasta_as_generator


class FragmentedSet:
    def __init__(self, fasta_filepath: str, max_seq_len: int, chunk_size: int = 10):
        filepath_comps = fasta_filepath.split(os.sep)
        self.set_name = filepath_comps[-1].split(".")[0]
        self.fasta_filepath = fasta_filepath
        self.max_seq_len = max_seq_len
        self.chunk_size = chunk_size
        self.generator = load_fasta_as_generator(fasta_filepath, chunk_size)

        # Initialize empty lists for ids, frags, and scopes
        self.ids: List[str] = []
        self.frags: List[str] = []
        self.scopes: List[int] = []

    def process_next_chunk(self) -> bool:
        try:
            chunk_ids, chunk_seqs = next(self.generator)
            chunk_frags, chunk_scopes = _fragment_sequences(chunk_seqs, self.max_seq_len)

            self.ids.extend(chunk_ids)
            self.frags.extend(chunk_frags)
            self.scopes.extend(chunk_scopes)

            return True
        except StopIteration:
            return False

    def process_all(self) -> None:
        while self.process_next_chunk():
            pass


def _fragment_sequences(sequences: List[str], max_seq_len: int) -> Tuple[List[str], List[int]]:
    frags = []
    scopes = []

    for seq in sequences:
        seq_len = len(seq)

        if seq_len > max_seq_len:
            frags_number = seq_len - max_seq_len + 1

            for i in range(frags_number):
                frags.append(seq[i:i + max_seq_len])

            scopes.append(frags_number)
        else:
            frags.append(seq)
            scopes.append(1)

    return frags, scopes
