import re
from nltk.stem.porter import PorterStemmer

class Stemmatizer:

    def stem(tokens): #this process aims to achieve the same goal as lemmatizing, but it might not return an acutal word
                      #whereas lemmatizing will.
        stemmer = PorterStemmer() #makes use of the Porter Stemmer algorithm
        stemmed_tokens = []
        for token in tokens:
            stemmed_token = ' '.join([stemmer.stem(w).strip("'") for w in token.split()])
            stemmed_tokens.append(stemmed_token)
        return stemmed_tokens
