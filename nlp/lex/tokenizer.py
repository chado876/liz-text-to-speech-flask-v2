import re
from nltk.util import ngrams
import nltk
from nltk import tokenize

class Tokenizer:

    def tokenize(string):
        pattern = re.compile(r"([-\s.,;!?])+") #identify tokens using -, all white space characters '\s', fullstops '.', commas ',',
                                               #semicolons ';', exclamation marks '!', and question signs '?' 
        tokens = pattern.split(string)  #split string into tokens using pattern
        tokens = [x for x in tokens if x and x not in '- \t\n.,;!?']   #remove pattern characters from list of tokens
        return tokens
    
    def sentence_tokenizer(string):
        return tokenize.sent_tokenize(string)   #split string into sentence tokens

    def n_gram_tokenize(n, tokens):
        n_gram_tokens = list(ngrams(tokens, n)) #gather n-grams, which is basically a sequence of N words
        return n_gram_tokens

    def remove_stop_words(tokens):
        nltk.download('stopwords')  #download nltk's stopword library
        stop_words = nltk.corpus.stopwords.words('english') #assign english stop words

        token_stop_words = [sw for sw in tokens if sw and sw in stop_words] #strip stop words from tokens
        return token_stop_words


    def normalize_tokens(tokens):       #normalization is basically converting all tokens to lowercase
        normalized_tokens = [token.lower() for token in tokens]
        return normalized_tokens


