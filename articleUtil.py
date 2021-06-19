from newspaper import Article
import nltk
import speechUtil as speechUtil
from random import randrange
from nlp.lex.lexical_analyzer import LexicalAnalyzer


def process_article(articleLink, fileName):
    article = Article(articleLink)
    article.download()
    article.parse()
    nltk.download('punkt')
    article.nlp()

    articleText = article.text
    randNum = randrange(1,900)
    
    speechUtil.synthesize_and_save_to_file(articleText, fileName)
    return articleText
    
