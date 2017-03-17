import urlparse

from bs4 import BeautifulSoup
import requests
from w3lib.url import canonicalize_url

resp = requests.get("http://www.ics.uci.edu/~lopes")
encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
soup = BeautifulSoup(resp.content, "html.parser")
if soup.find('html') is not None:
    for link in soup.find_all('a', href=True):
        parsed = urlparse(link['href'])
        url = parsed.netloc + parsed.path + "?" + parsed.query
        url = canonicalize_url(url)
        if url[len(url) - 1] == '/':
            url = url[:len(url) - 1]

