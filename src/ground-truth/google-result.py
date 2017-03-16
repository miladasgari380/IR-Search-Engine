from google import search

def go(query):
    query += " site:ics.uci.edu"
    for url in search(query, tld='es', lang='es', stop=10):
        print url

go("armin balalaie")