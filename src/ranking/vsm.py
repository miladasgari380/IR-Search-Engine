import math
import pickle

from constants import NUMBER_OF_DOCUMENTS, VSM_FILE
from indexing.indexer import load_inverted_index

vsm = dict()


def save_vector_space_model():
    with open(VSM_FILE, 'wb') as f:
        pickle.dump(vsm, f, pickle.HIGHEST_PROTOCOL)


def load_vector_space_model():
    with open(VSM_FILE, 'r') as f:
        return pickle.load(f)


def create_vector_space_model():
    inverted_index = load_inverted_index()
    print "read finished"
    counter = 0

    for word,docs in inverted_index.iteritems():
        for doc_id,postings in docs.iteritems():
            if not vsm.has_key(doc_id):
                vsm[doc_id] = dict()
            vsm[doc_id][word] = len(postings)
        counter += 1
        if counter % 1000 == 0: print counter

    print "reached"
    counter = 0
    for doc_id,words in vsm.iteritems():
        for word,word_frequency in words.iteritems():
            idf = math.log(NUMBER_OF_DOCUMENTS*1.0 / len(inverted_index[word].keys()))
            tf = 0.5 + (0.5 * (word_frequency*1.0 / max(words.values())))
            vsm[doc_id][word] = tf*idf
        counter += 1
        if counter%100==0:
            print counter

    save_vector_space_model()


def normalize_vsm():
    global vsm
    counter =0
    vsm = load_vector_space_model()
    for doc_id,words in vsm.iteritems():
        for word,tfidf in words.iteritems():
            vsm[doc_id][word] /= math.sqrt(sum([math.pow(x,2) for x in words.values()]))

        counter += 1
        if counter % 500 == 0:
            print counter
    save_vector_space_model()

# normalize_vsm()
# create_vector_space_model()
vsm = load_vector_space_model()
pass