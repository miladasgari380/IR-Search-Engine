import os
import pickle

from constants import RAW_DATA_BASE_PATH, HTML_DICT_FIELDS_WEIGHT, INVERTED_INDEX_FILE
from indexing.html_parser import document_id, transform_html_to_dict, store_html_dict
from indexing.tokenizer import tokenize

inverted_index = {}


def save_inverted_index():
    pickle.dump(inverted_index, INVERTED_INDEX_FILE, pickle.HIGHEST_PROTOCOL)


def load_inverted_index():
    return pickle.load(INVERTED_INDEX_FILE)


def main():
    global inverted_index

    for folder_name in os.listdir(os.path.join(os.getcwd(), RAW_DATA_BASE_PATH)):
        if folder_name.isdigit():
            if int(folder_name) == 0: #remove in future
                print "in folder: " + folder_name
                for file_name in os.listdir(os.path.join(os.getcwd(), RAW_DATA_BASE_PATH, folder_name)):
                    if file_name.isdigit():
                        if int(file_name) == 3: #remove in future
                            print "in file: " + file_name
                            doc_id = document_id(folder_name,file_name)
                            html_dict = transform_html_to_dict(doc_id)
                            store_html_dict(doc_id, html_dict)

                            for field in HTML_DICT_FIELDS_WEIGHT:
                                if html_dict[field[0]] is None: continue
                                for token,offset in tokenize(html_dict[field[0]]):
                                    if not inverted_index.has_key(token):
                                        inverted_index[token] = {}

                                    if not inverted_index[token].has_key(doc_id):
                                        inverted_index[token][doc_id] = []

                                    inverted_index[token][doc_id].append((field,offset))
    save_inverted_index()

if __name__ == "__main__":
    main()