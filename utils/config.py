import os

MODEL_NAME = "ProteinBERT"
ADDED_TOKENS_PER_SEQ = 2
SEQ_CUTOFF = 40
MODEL_PATH = 'models'
FASTA_PATH = 'fasta'
ALL_AAS = 'ACDEFGHIKLMNPQRSTUVWXY'
ADDITIONAL_TOKENS = ['<OTHER>', '<START>', '<END>', '<PAD>']

PREDS_PATH = "/app/output"
SEP = "\t"


def makedir(dirpath: str) -> str:
    if len(os.path.split(dirpath)) > 1:
        directory = os.path.dirname(dirpath)
    else:
        directory = dirpath
    os.makedirs(directory, exist_ok=True)
    return dirpath
