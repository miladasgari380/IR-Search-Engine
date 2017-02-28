def transform_html_to_dict(document_id):
    pass

def unpack_document_id(document_id):
    pass

def document_id(dir_name, file_name):
    pass

def store_html_dict(document_id, html_dict):
    pass

def load_html_dict(document_id):
    pass

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
# def indexer(file_dict, extracted, type):
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
# inverted_index = indexer(inverted_index, extracted, 'p')

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