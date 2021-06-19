import nltk
from nltk.stem import WordNetLemmatizer

class Lemmatizer:
    
    def lemmatize(tokens):      #this process is to basically remove inflectional endings and return the base of a word
                                # eg. 'rocks' is lemmatized to 'rock'
        nltk.download('wordnet')
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = []
        for token in tokens:
            lemmatized_tokens.append(lemmatizer.lemmatize(token))
        
        return lemmatized_tokens