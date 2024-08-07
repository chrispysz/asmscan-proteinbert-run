from typing import List, Tuple, Generator

from Bio import SeqIO


def load_fasta_as_generator(file_path: str, chunk_size: int = 1000) -> Generator[
    Tuple[List[str], List[str]], None, None]:
    """Read a FASTA file and yield chunks of ids and sequences."""
    ids = []
    sequences = []
    with open(file_path, "r") as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            ids.append(str(record.id))
            sequences.append(str(record.seq))

            if len(ids) >= chunk_size:
                yield ids, sequences
                ids = []
                sequences = []

    # Yield any remaining data
    if ids:
        yield ids, sequences
