#This module prepares the data for the RNN

import nltk

VOCAB_SIZE = 8000
UNKNOWN_TOKEN = "__UNKNOWN_TOKEN__"

def tokenize(string):
    very_obscure_string = " NEWLINENEWLINENEWLINE "
    #preserve newlines
    string.replace('\n',very_obscure_string)
    tokens = nltk.word_tokenize(string);
    return ['\n' if token == very_obscure_string.strip() else token for token in tokens]

def get_tokens(filename):
    with open(filename,'r') as f:
        poems = f.read().split("__END__")
    tokenized_poems = [tokenize(poem).append("__END__") for poem in poems]
    token_freq = nltk.FreqDist(itertools.chain(*tokenized_poems))
    print(len(token_freq.items()),"unique tokens")

    vocab = token_freq.most_common(VOCAB_SIZE - 1)
    index_to_token = [x[0] for x in vocab]
    index_to_token.append(UNKNOWN_TOKEN)
    token_to_index = dict([(t,i) for i,t in enumerate(index_to_token)])

    print("Using vocabulary size",VOCAB_SIZE)
    print("The least frequent word in vocabulary is:",vocab[-1][0],"\nIt appears",vocab[-1][1],"times")

    for i,poem in enumerate(tokenized_poems):
        tokenized_poems[i] = [t if t in token_to_index else UNKNOWN_TOKEN for t in poem]

    print("Sample poem:",poems[0],"Sample prepped:",tokenized_poems[0],sep='\n')
