import os
import pickle

from google import search


def go():
    dic = dict()
    queries = ['mondego', 'machine learning', 'software engineering', 'security', 'student affairs', 'graduate courses',
               'Crista Lopes', 'REST', 'computer games', 'information retrieval']
    for query in queries:
        dic[query] = list()
    for query in queries:
        query += " site:ics.uci.edu -inurl:pdf"
        for url in search(query, tld='es', lang='es', stop=5):
            dic[query].append(url)

    with open('google-results', 'wb') as google_dic:
        pickle.dump(dic, google_dic, pickle.HIGHEST_PROTOCOL)

go()