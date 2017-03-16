import json
import math
import pickle

import operator

from constants import NUMBER_OF_DOCUMENTS, VSM_FILE, URL_FILE
from indexing.html_parser import cleanup_text, load_html_dict
from indexing.indexer import load_inverted_index
from indexing.tokenizer import tokenize

vsm = dict()


def save_vector_space_model():
    with open(VSM_FILE, 'wb') as f:
        pickle.dump(vsm, f, pickle.HIGHEST_PROTOCOL)


def load_vector_space_model():
    with open(VSM_FILE, 'r') as f:
        return pickle.load(f)


def create_vector_space_model():
    global inverted_index

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
        max_value = max(words.values())
        for word,word_frequency in words.iteritems():
            idf = math.log(NUMBER_OF_DOCUMENTS*1.0 / len(inverted_index[word].keys()))
            tf = 0.5 + (0.5 * (word_frequency*1.0 / max_value))
            # tf = 1 + math.log(word_frequency*1.0)
            vsm[doc_id][word] = tf*idf
        counter += 1
        if counter%100==0:
            print counter
    normalize_vsm()
    save_vector_space_model()


def normalize_vsm():
    global vsm
    counter =0
    # vsm = load_vector_space_model()
    for doc_id,words in vsm.iteritems():
        for word,tfidf in words.iteritems():
            vsm[doc_id][word] /= math.sqrt(sum([math.pow(x,2) for x in words.values()]))

        counter += 1
        if counter % 500 == 0:
            print counter
    # save_vector_space_model()


def calculate_similarity(vector1,vector2):
    return sum([vector1[word]*vector2[word]*1.0 for word in set(vector1.keys()) & set(vector2.keys())])


def search_vsm(query):
    global inverted_index
    global vsm

    query = tokenize(cleanup_text(query))
    if not query:
        return []

    query_vector = dict()
    for word,offset in query:
        if inverted_index.has_key(word):
            idf = math.log(NUMBER_OF_DOCUMENTS * 1.0 / len(inverted_index[word].keys()))
            tf = 1.0
            query_vector[word] = tf * idf

    if not query_vector:
        return []

    doc_ids = set()
    for word in query_vector.keys():
        doc_ids = doc_ids.union(inverted_index[word].keys())

    ranked_results = []

    for doc_id in doc_ids:
        ranked_results.append((doc_id,calculate_similarity(vsm[doc_id],query_vector)))

    ranked_results = sorted(ranked_results, key=operator.itemgetter(1))
    ranked_results = [ranked_result[0] for ranked_result in ranked_results]
    return ranked_results[:10]


def get_pages_information(doc_ids):
    global file_to_url_dict

    pages_info = []

    for doc_id in doc_ids:
        doc_html_dict = load_html_dict(doc_id)
        pages_info.append({
            'doc_id': doc_id,
            'url': file_to_url_dict[doc_id],
            'title': doc_html_dict['title'][:50] if doc_html_dict['title'] else '<no-title>',
            'body': doc_html_dict['body'][:100]
        })

    return pages_info


def search(query):
    if not query:
        return []
    return get_pages_information(search_vsm(query))


def load_url_dict():
    with open(URL_FILE) as f:
        return json.load(f)

print "SVM has been loaded!"
inverted_index = load_inverted_index()
# normalize_vsm()
create_vector_space_model()
# vsm = load_vector_space_model()
print "Inverted Index has been loaded!"
# file_to_url_dict = load_url_dict()
print "URL dict has been loaded!"
