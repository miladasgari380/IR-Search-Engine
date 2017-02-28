from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize


def tokenize(s):
    words = word_tokenize(s)
    return words


def stemmer(s):
    ps = PorterStemmer()
    return ps.stem(s)


def stop_word_eliminator(s):
    stop = set(stopwords.words('english'))
    without_stop = [i for i in s.lower().split() if i not in stop]
    return without_stop
