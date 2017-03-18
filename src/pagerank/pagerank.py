import pickle
from urlparse import urlparse
import io
import json
from bs4 import BeautifulSoup
import requests
from w3lib.url import canonicalize_url
from constants import URL_FILE, RAW_DATA_BASE_PATH, PAGERANK_FILE
import networkx as nx
from lxml import html

from indexing.html_parser import unpack_document_id


def load_file_to_url_dict():
    with open(URL_FILE) as f:
        temp_dict = json.load(f)
    file_to_url = dict()
    for key, val in temp_dict.items():
        file_to_url[key] = cleanup_url(val)
    return file_to_url

def load_url_to_file_dict():
    with open(URL_FILE) as f:
        temp_dict = json.load(f)
    url_to_file = dict()
    for key, val in temp_dict.items():
        url_to_file[cleanup_url(val)] = key
    return url_to_file

def cleanup_url(url):
    parsed = urlparse(url)
    url = parsed.netloc + parsed.path + "?" + parsed.query
    url = canonicalize_url(url)
    if url[len(url) - 1] == '/':
        url = url[:len(url) - 1]
    return url

def save_pagerank(pr):
    with open(PAGERANK_FILE, 'wb') as f:
        pickle.dump(pr, f, pickle.HIGHEST_PROTOCOL)

def load_pagerank():
    with open(PAGERANK_FILE, 'r') as f:
        return pickle.load(f)


if __name__ == "__main__":
    file_to_url_dict = load_file_to_url_dict()
    url_to_file_dict = load_url_to_file_dict()
    G = nx.DiGraph()
    count = 0

    for file, url in file_to_url_dict.items():
        folder_name, file_name = unpack_document_id(file)
        count += 1
        # if folder_name == "0" and int(file_name) < 50:
        data_file = None
        try:
            with io.open(RAW_DATA_BASE_PATH+"/"+folder_name+"/"+file_name, "r", encoding='utf8') as data_file:
                data = data_file.read()
        except Exception:
            # print "Not found", folder_name,'/', file_name
            continue

        if file not in G.nodes():
            G.add_node(file)

        if count%1000 == 0:
            print count

        # Parsing HTML content to extract links
        try:
            tree = html.fromstring(data)
            raw_links = tree.xpath('//a/@href')
        except Exception:
            continue

        default_scheme = urlparse(url).scheme

        for link in raw_links:
            if len(link) < 2: continue
            # Make absolute links
            parsed = urlparse(link)
            if parsed.scheme not in ["","http", "https"]:
                continue
            if link[0] is "/":
                if link[1] is "/": # starts with //
                    absolute_url = default_scheme + ":" + link
                else: # starts with /
                    absolute_url = default_scheme + "://" + urlparse(url).netloc + link
            elif parsed.netloc is "":
                rslash_pos = url.rfind("/")
                if rslash_pos is -1:
                    absolute_url = url + "/" + link
                else:
                    absolute_url = url[:rslash_pos+1] + link
            else:
                absolute_url = link

            absolute_url = cleanup_url(absolute_url)

            if url != absolute_url:
                if url_to_file_dict.has_key(absolute_url):
                    if url_to_file_dict[absolute_url] not in G.nodes():
                        G.add_node(url_to_file_dict[absolute_url])
                    G.add_edge(file, url_to_file_dict[absolute_url])

    pr = nx.pagerank(G, alpha=0.9)
    save_pagerank(pr)


    # nx.draw(G)

