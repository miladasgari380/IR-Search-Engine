# encoding: utf-8

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.regexp import wordpunct_tokenize

wnl = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def tokenize(text):
    ret = []
    last_offset = 0
    if not text:
        return ret
    for token in wordpunct_tokenize(text):
        processed_token = token.lower().strip()
        if not processed_token or len(processed_token)<3 or is_stop_word(token):
            continue
        processed_token = lemmatize_word(processed_token)
        last_offset = text.find(token, last_offset)
        ret.append((processed_token, last_offset))
    return ret


def stem_word(word):
    if word:
        return PorterStemmer().stem(word)
    return ''


def lemmatize_word(word):
    global wnl
    if word:
        return wnl.lemmatize(word)
    return ''

def is_stop_word(word):
    return word in stop_words


