import prep
import numpy as np
import keras

VOCAB_SIZE = 8000
seq_length = 0

def load_data(filename):
    seqs,index_to_token,token_to_index = prep.get_sequences(filename,VOCAB_SIZE)
    seq_length = len(seqs[0])
    seq_count = len(seqs)

    x = np.zeros(seq_count,seq_length,VOCAB_SIZE)
    y = np.zeros(seq_count,seq_length,VOCAB_SIZE)

    for seq in seqs:
