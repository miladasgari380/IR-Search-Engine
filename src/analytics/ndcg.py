import pickle
from urlparse import urlparse

from google import search
from w3lib.url import canonicalize_url
import math

from constants import GOOGLE_FILE
from pagerank.pagerank import load_file_to_url_dict, cleanup_url


def google_search(query):
    ans = list()
    query += " site:ics.uci.edu -inurl:pdf"
    for url in search(query, tld='es', lang='es', stop=5):
        ans.append(url)
    return ans


def calculate_ndcg_5(our_urls, query):
    # google_results = google_search(query)
    with open(GOOGLE_FILE, 'r') as google_dic:
        google_results_dic = pickle.load(google_dic)

    google_results = google_results_dic[query]
    google_results = get_five_best_from_google(google_results)

    ndcg = 0

    for i in range(len(our_urls)):
        for j in range(len(google_results)):
            if cleanup_url(our_urls[i]) == cleanup_url(google_results[j]):
                ndcg += ((5.0 - j) / (math.log(i + 2)))
                break
    
    return (ndcg/sum(range(len(google_results),0, -1)))


# def remove_proto_from_url(url):
#     parsed = urlparse(url)
#     url = parsed.netloc+parsed.path+"?"+parsed.query
#     url = canonicalize_url(url)
#     if url[len(url) - 1] == '/':
#         url = url[:len(url)-1]
#
#     # print "aft",url
#     return url

def get_five_best_from_google(google_results):
    ans = list()
    file_to_url = load_file_to_url_dict()
    for google_link in google_results:
        if google_link in file_to_url.values():
            ans.append(google_link)
        if len(ans >= 5):
            return ans
    return ans
