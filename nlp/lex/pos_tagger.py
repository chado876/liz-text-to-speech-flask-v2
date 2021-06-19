import nltk
from nltk.tokenize import word_tokenize

class PosTagger:

    def tag_pos(tokens):    ##returns tokens with their part of speech in a tuple - makes use of nltk pos library
        pos_tokens = nltk.pos_tag(tokens)
        return pos_tokens
    