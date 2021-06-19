import re
import nltk
from nltk import tokenize
import demo_parser as parser

class LexicalAnalyzer:
    
    def lexical_analysis(string):
        tokens = LexicalAnalyzer.tokenize(string)
        pos_tokens = LexicalAnalyzer.pos_tagger(tokens)
        normalized_tokens = LexicalAnalyzer.normalize(tokens)
        tokenized_sentences = LexicalAnalyzer.tokenize_by_sentence(string)
        pos_tagged_sentences = LexicalAnalyzer.pos_tag_sentences(tokenized_sentences)

        print("Normalized Tokens:", normalized_tokens)
        print("Tokenized Sentences:", tokenized_sentences)
        print("POS Tagged Tokenized Sentences:", pos_tagged_sentences)

        parser.parse(pos_tagged_sentences)


    def tokenize(string):
        
        pattern = re.compile(r"([-\s.,;!?])+")
        tokens = pattern.split(string)

        new_tokens = [token for token in tokens if token and token not in '- \t\n.,;!?']
        print(tokens)
        print(new_tokens)
        return new_tokens

    def tokenize_by_sentence(string):
        tokenized_sentences = nltk.sent_tokenize(string)
        return tokenized_sentences

        

    
    def pos_tagger(tokens):
        pos_tagged_tokens = nltk.pos_tag(tokens)
        print(pos_tagged_tokens)
        return pos_tagged_tokens
    
    def normalize(tokens):
        normalized_tokens = []

        for token in tokens:
            normalized_token = token.lower()
            normalized_tokens.append(normalized_token)
        
        return normalized_tokens

    
    def pos_tag_sentences(sentences):
        pos_tagged_sentences = []
        for sentence in sentences:
            pos_tagged_sentence = LexicalAnalyzer.pos_tagger(LexicalAnalyzer.tokenize(sentence))
            pos_tagged_sentences.append(pos_tagged_sentence)
        return pos_tagged_sentences



test_string = "This is some test string . 3."
LexicalAnalyzer.lexical_analysis(test_string)