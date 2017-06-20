#This module prepares the data for the RNN

import nltk
import itertools

UNKNOWN_TOKEN = "__UNKNOWN_TOKEN__"

def tokenize(string):
    very_obscure_string = " NEWLINENEWLINENEWLINE "
    #preserve newlines
    string.replace('\n',very_obscure_string)
    tokens = nltk.word_tokenize(string);
    return ['\n' if token == very_obscure_string.strip() else token for token in tokens]




def get_sequences(filename,vocab_size):
    with open(filename,'r') as f:
        poems = f.read().split("__END__")
    tokenized_poems = [tokenize(poem).append("__END__") for poem in poems]

    maxlen = 0
    for poem in poems:
        maxlen = len(poem) if len(poem) > maxlen else maxlen

    for poem in poems:
        while len(poem) < maxlen:
            poem.append('')

    token_freq = nltk.FreqDist(itertools.chain(*tokenized_poems))
    print(len(token_freq.items()),"unique tokens")

    vocab = token_freq.most_common(vocab_size - 1)
    index_to_token = [x[0] for x in vocab]
    index_to_token.append(UNKNOWN_TOKEN)
    token_to_index = dict([(t,i) for i,t in enumerate(index_to_token)])

    print("Using vocabulary size",VOCAB_SIZE)
    print("The least frequent word in vocabulary is:",vocab[-1][0],"\nIt appears",vocab[-1][1],"times")

    for i,poem in enumerate(tokenized_poems):
        tokenized_poems[i] = [t if t in token_to_index else UNKNOWN_TOKEN for t in poem]

    return (tokenized_poems,index_to_token,token_to_index) 

    print("Sample poem:",poems[0],"Sample prepped:",tokenized_poems[0],sep='\n')
