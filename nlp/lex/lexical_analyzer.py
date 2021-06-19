from .tokenizer import Tokenizer
from .lemmatizer import Lemmatizer
from .pos_tagger import PosTagger
from .stemmer import Stemmatizer
from ..parse.parser import Parser

class LexicalAnalyzer:

  def perform_lexical_analysis(string):
      sentences = Tokenizer.sentence_tokenizer(string) #split text into sentences
      tokens = Tokenizer.tokenize(string)
      two_gram_tokens = Tokenizer.n_gram_tokenize(2, tokens)
      stop_words = Tokenizer.remove_stop_words(tokens)
      normalized_tokens = Tokenizer.normalize_tokens(tokens)
      lemmatized_tokens = Lemmatizer.lemmatize(tokens)
      tokens_pos = PosTagger.tag_pos(tokens)
      stemmed_tokens = Stemmatizer.stem(tokens)

      print('\033[94m============SENTENCES============\033[0m \n ', sentences)
      print('\n\033[94m============TOKENS============\033[0m \n ', tokens)
      print('\n\033[94m============BI-GRAMS============\033[0m \n ', two_gram_tokens)
      print('\n\033[94m============STOP WORDS============\033[0m \n ', stop_words)
      print('\n\033[94m============NORMALIZED TOKENS============\033[0m \n ', normalized_tokens)
      print('\n\033[94m============LEMMATIZED TOKENS============\033[0m \n ', lemmatized_tokens)
      print('\n\033[94m============PARTS OF SPEECH============\033[0m \n', tokens_pos)
      print('\n\033[94m============STEMMATIZED TOKENS============\033[0m \n', stemmed_tokens)
      
      pos_sentences = []
      
      for sentence in sentences:
        pos_sentence = (PosTagger.tag_pos(Tokenizer.tokenize(sentence)))
        pos_sentences.append(pos_sentence)

      return pos_sentences


