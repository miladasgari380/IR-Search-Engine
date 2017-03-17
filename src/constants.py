RAW_DATA_BASE_PATH = '../../raw-data'
INDEXED_DATA_BASE_PATH = '../../indexed-data'
INVERTED_INDEX_FILE = INDEXED_DATA_BASE_PATH + '/inverted_index'
VSM_FILE = INDEXED_DATA_BASE_PATH + '/vsm'
URL_FILE = RAW_DATA_BASE_PATH + '/bookkeeping.json'
GOOGLE_FILE = INDEXED_DATA_BASE_PATH + '/google-results'
PAGERANK_FILE = INDEXED_DATA_BASE_PATH + '/pagerank'


NUMBER_OF_DOCUMENTS = 34306

HTML_DICT_FIELDS_WEIGHT = {
    "title": 50,
    "keywords": 30,
    "description": 30,
    "body": 1
}