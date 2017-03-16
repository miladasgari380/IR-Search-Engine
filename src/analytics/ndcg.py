from urlparse import urlparse

from google import search
from w3lib.url import canonicalize_url
import math


def google_search(query):
    ans = list()
    query += " site:ics.uci.edu"
    for url in search(query, tld='es', lang='es', stop=10):
        ans.append(url)
    return ans


def calculate_ndcg_5(our_urls, query):
    google_results = google_search(query)

    ndcg = 0
    for i in range(len(our_urls)):
        for j in range(len(google_results)):
            if remove_proto_from_url(our_urls[i]) == remove_proto_from_url(google_results[j]):
                ndcg += ((5.0 - j) / (math.log(i + 1)))
                break
    
    return (ndcg/sum(range(len(google_results),0, -1)))


def remove_proto_from_url(url):
    parsed = urlparse(url)
    url = parsed.netloc+parsed.path+"?"+parsed.query
    url = canonicalize_url(url)
    print "aft",url
    return url