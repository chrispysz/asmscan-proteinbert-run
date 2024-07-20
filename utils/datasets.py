import random
from typing import List, Tuple

import pandas as pd
from Bio import SeqIO


def load_fasta_as_lists(file_path: str) -> Tuple[List[str], List[str]]:
    """Read a FASTA file and return a tuple of ids and sequences."""
    ids = []
    sequences = []
    with open(file_path, "r") as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            ids.append(str(record.id))
            sequences.append((str(record.seq)))
    return ids, sequences


def _read_fasta(file_path: str, label: int):
    """Read a FASTA file and return a list of (sequence, label) tuples."""
    sequences = []
    with open(file_path, "r") as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequences.append((str(record.seq), label))
    return sequences


def _combine_and_shuffle(sequences1: List[Tuple[str, int]], sequences2: List[Tuple[str, int]]):
    """Combine two lists of sequences, shuffle them, and return a DataFrame."""
    combined = sequences1 + sequences2
    random.shuffle(combined)
    return pd.DataFrame(combined, columns=['seq', 'label'])


