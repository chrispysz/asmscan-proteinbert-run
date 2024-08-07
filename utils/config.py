import os

MODEL_NAME = "ProteinBERT"
ADDED_TOKENS_PER_SEQ = 2
SEQ_CUTOFF = 40
MODEL_PATH = 'models'
ALL_AAS = 'ACDEFGHIKLMNPQRSTUVWXY'
ADDITIONAL_TOKENS = ['<OTHER>', '<START>', '<END>', '<PAD>']

SEP = "\t"
GO_SIZE = 8943


def makedir(dirpath: str) -> str:
    if len(os.path.split(dirpath)) > 1:
        directory = os.path.dirname(dirpath)
    else:
        directory = dirpath
    os.makedirs(directory, exist_ok=True)
    return dirpath
