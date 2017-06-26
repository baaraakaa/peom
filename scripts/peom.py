import prep
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.layers.wrappers import TimeDistributed
from keras.callbacks import ModelCheckpoint
import argparse
from RNN_utils import *

VOCAB_SIZE = 8000

ap = argparse.ArgumentParser()
ap.add_argument('-data_dir', default='./data/test.txt')
ap.add_argument('-batch_size', type=int, default=50)
ap.add_argument('-layer_num', type=int, default=2)
ap.add_argument('-hidden_dim', type=int, default=500)
ap.add_argument('-mode', default='new')
ap.add_argument('-weight_file', default='weights.best.hdf5')
args = vars(ap.parse_args())

DATA_DIR = args['data_dir']
BATCH_SIZE = args['batch_size']
HIDDEN_DIM = args['hidden_dim']
WEIGHT_FILE = args['weight_file']
LAYER_NUM = args['layer_num']

def load_data(filename):
    seqs,index_to_token,token_to_index = prep.get_sequences(filename,VOCAB_SIZE)
    seq_length = len(seqs[0])
    seq_count = len(seqs)

    x = np.zeros((seq_count,seq_length,VOCAB_SIZE))
    y = np.zeros((seq_count,seq_length,VOCAB_SIZE))

    for i,seq in enumerate(seqs):
        x_seq_ix = [token_to_index[token] for token in seq]
        input_seq = np.zeros((seq_length,vocab_size))
        for j in range(seq_length):
            input_seq[j][x_seq_ix[j]] = 1
        x[i] = input_seq

        y_seq = seq[1:].append('')
        y_seq_ix = [token_to_index[token] for token in y_seq]
        target_seq = np.zeros((seq_length,VOCAB_SIZE))
        for j in range(seq_length):
            target_seq[j][x_seq_ix[j]] = 1
        y[i] = target_seq

    return (x,y,index_to_token,seq_length)

def init_model():
    model = Sequential()
    model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
    for i in range(LAYER_NUM - 1):
      model.add(LSTM(HIDDEN_DIM, return_sequences=True))
    model.add(TimeDistributed(Dense(VOCAB_SIZE)))
    model.add(Activation('softmax'))
    if mode == 'load' or mode == 'gen':
        model.load_weights(WEIGHT_FILE)
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")
    return model

def train(x,y,model):
    checkpoint = ModelCheckpoint(WEIGHT_FILE,monitor='val_acc',verbose=1,save_best_only=True,mode = 'max')
    callback_list = [checkpoint]
    while true:
        model.fit(x,y,batch_size=BATCH_SIZE,callbacks=callback_list,verbose=1)

def generate(model,seq_length,index_to_token):
    ix = [np.random.randint(VOCAB_SIZE)]
    y_tok = [index_to_token[ix[-1]]]
    x = np.zeros((1,seq_length,VOCAB_SIZE))
    for i in range(seq_length):
        x[0,i,:][ix[-1]] = 1
        next_tok = index_to_token[ix[-1]]
        if next_tok not == '\n':
            print(index_to_token[ix[-1]],end="")
        else print()
        ix = np.argmax(model.predict(x[:,:i+1,:])[0],1)
        y_tok.append(index_to_token[ix[-1]])
    return y_tok

def run():
    x,y,index_to_token,seq_length = load_data(DATA_DIR)
    model = init_model()
    if mode == 'gen':
        generate(model,seq_length,index_to_token)
    else train(x,y,model)

if __name__ == '__main__':
    run()
