RAW_DATA_BASE_PATH = '../../raw-data'
INDEXED_DATA_BASE_PATH = '../../indexed-data'
INVERTED_INDEX_FILE = INDEXED_DATA_BASE_PATH + '/inverted_index'
VSM_FILE = INDEXED_DATA_BASE_PATH + '/vsm'
URL_FILE = RAW_DATA_BASE_PATH + '/bookkeeping.json'

NUMBER_OF_DOCUMENTS = 34306

HTML_DICT_FIELDS_WEIGHT = [
    ("title", 2),
    ("keywords", 1),
    ("description", 1),
    ("body", 1)
]