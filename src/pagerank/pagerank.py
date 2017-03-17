import pickle
from urlparse import urlparse
import io
import json
from bs4 import BeautifulSoup
import requests
from w3lib.url import canonicalize_url
from constants import URL_FILE, RAW_DATA_BASE_PATH, PAGERANK_FILE
import networkx as nx

from indexing.html_parser import unpack_document_id


def load_url_dict():
    with open(URL_FILE) as f:
        return json.load(f)


def save_pagerank(pr):
    with open(PAGERANK_FILE, 'wb') as f:
        pickle.dump(pr, f, pickle.HIGHEST_PROTOCOL)


def load_pagerank():
    with open(PAGERANK_FILE, 'r') as f:
        return pickle.load(f)


if __name__ == "__main__":
    file_to_url_dict = load_url_dict()
    url_to_file_dict = dict()
    G = nx.DiGraph()
    count = 0

    for key, val in file_to_url_dict.items():
        url_to_file_dict[val] = key

    for key, val in file_to_url_dict.items():
        # resp = requests.get(val)
        folder_name, file_name = unpack_document_id(key)
        count += 1
        # if folder_name == "0" and int(file_name) < 50:
        data_file = None
        try:
            with io.open(RAW_DATA_BASE_PATH+"/"+folder_name+"/"+file_name, "r", encoding='utf8') as data_file:
                data = data_file.read()
        except Exception:
            # print "Not found", folder_name,'/', file_name
            continue

        if count%1000 == 0:
            print count
        # encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(data, "html.parser")
        if soup.find('html') is not None:
            if key not in G.nodes():
                G.add_node(key)
            for link in soup.find_all('a', href=True):
                parsed = link.get('href',None)
                parsed = urlparse(parsed)
                url = parsed.netloc + parsed.path + "?" + parsed.query
                url = canonicalize_url(url)
                if url[len(url) - 1] == '/':
                    url = url[:len(url) - 1]
                if url != val:
                    if url_to_file_dict.has_key(url):
                        if url_to_file_dict[url] not in G.nodes():
                            G.add_node(url_to_file_dict[url])
                        G.add_edge(key, url_to_file_dict[url])
    pr = nx.pagerank(G, alpha=0.9)
    save_pagerank(pr)


    # nx.draw(G)

