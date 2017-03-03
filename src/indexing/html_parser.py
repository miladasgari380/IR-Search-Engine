import os
import io
import re
import pickle
from bs4 import BeautifulSoup
from constants import RAW_DATA_BASE_PATH, INDEXED_DATA_BASE_PATH



def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    # elif re.match("<!--.*-->", str(element)):
    #     return False
    return True


def transform_html_to_dict(document_id):
    html_dict = {}
    folder_name, file_name = unpack_document_id(document_id)
    with io.open(RAW_DATA_BASE_PATH+"/"+folder_name+"/"+file_name, "r", encoding='utf8') as data_file:
        data = data_file.read()
        soup = BeautifulSoup(data, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()

        if soup.find('html') is None:  # Non html files
            # print "Not HTML file!"
            return None

        if soup.title is not None:
            html_dict['title'] = soup.title.string
        else:
            html_dict['title'] = None
        desc = soup.find_all(attrs={"name": "description"})
        if len(desc) > 0 and desc[0].has_key("content"):
            html_dict['description'] = cleanup_text(desc[0]['content'])
        else:
            html_dict['description'] = None
        keywords = soup.find_all(attrs={"name": "keywords"})
        if len(keywords) > 0 and keywords[0].has_key("content"):
            html_dict['keywords'] = cleanup_text(keywords[0]['content'])
        else:
            html_dict['keywords'] = None

        for script in soup(["title"]):
            script.extract()

        text = soup.get_text()
        html_dict['body'] = cleanup_text(text)
    return html_dict


# TODO: Change regular expression to not delete non-english words
# TODO: We need to decide here what should be indexed
def cleanup_text(text):
    regex = re.compile('[^a-zA-Z0-9\'_-]')
    text = regex.sub(' ', text)
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return ' '.join(chunk for chunk in chunks if chunk)


def unpack_document_id(doc_id):
    file_folder_info = doc_id.split("/")
    return file_folder_info[0], file_folder_info[1]


def document_id(dir_name, file_name):
    return dir_name+"/"+file_name


def store_html_dict(doc_id, html_dict):
    folder_name, file_name = unpack_document_id(doc_id)

    if not os.path.exists(os.path.join(INDEXED_DATA_BASE_PATH, folder_name)):
        os.makedirs(os.path.join(INDEXED_DATA_BASE_PATH, folder_name))
    with open(os.path.join(INDEXED_DATA_BASE_PATH, folder_name, file_name), 'wb') as indexed_doc:
        pickle.dump(html_dict, indexed_doc, pickle.HIGHEST_PROTOCOL)


def load_html_dict(doc_id):
    folder_name, file_name = unpack_document_id(doc_id)
    with open(os.path.join(INDEXED_DATA_BASE_PATH, folder_name, file_name), 'r') as indexed_doc:
        return pickle.load(indexed_doc)


# def element_extractor(file, elements_list):
#     data = {}
#     for element_type in elements_list:
#         if element_type not in data.keys():
#             data[element_type] = list()
#         for element in file.find_all(element_type):
#             data[element_type].append(element.get_text())
#     # json_data = json.dumps(data)
#     return data
#
#
# def indexing(file_dict, extracted, type):
#     for i in range(len(extracted[type])):
#         stopwords_removed = stop_word_eliminator(extracted[type][i])
#         for token in stopwords_removed:
#             stemmed_token = stemmer(token)
#             if stemmed_token not in file_dict.keys():
#                 file_dict[stemmed_token] = list()
#             info = dict()
#             info[type] = i
#             file_dict[stemmed_token].append(info)
#
#             # {token1: [{p:1}, {p:5}]}
#
#     return file_dict
#
# soup = BeautifulSoup(data, "html.parser")
# if soup.find('html') == None:  # Non html files
#     continue
# for script in soup(["script", "style"]):
#     script.extract()
# # print soup.prettify()
# extracted = element_extractor(soup, ['p'])
# inverted_index = indexing(inverted_index, extracted, 'p')

# print list(soup.children)

# text = soup.get_text()
# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)
# print text
#
# print data_file