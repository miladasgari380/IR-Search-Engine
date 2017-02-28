import os
import re
import json
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# keep location of each token

dataPath = '../../raw-data'
indexedDocumentsPath = '../../indexed-data'


def tokenizer(s):
    words = word_tokenize(s)
    return words


def stemmer(s):
    ps = PorterStemmer()
    return ps.stem(s)


def stop_word_eliminator(s):
    stop = set(stopwords.words('english'))
    without_stop = [i for i in s.lower().split() if i not in stop]
    return without_stop


def element_extractor(file, elements_list):
    data = {}
    for element_type in elements_list:
        if element_type not in data.keys():
            data[element_type] = list()
        for element in file.find_all(element_type):
            data[element_type].append(element.get_text())
    # json_data = json.dumps(data)
    return data


def indexer(file_dict, extracted, type):
    for i in range(len(extracted[type])):
        stopwords_removed = stop_word_eliminator(extracted[type][i])
        for token in stopwords_removed:
            stemmed_token = stemmer(token)
            if stemmed_token not in file_dict.keys():
                file_dict[stemmed_token] = list()
            info = dict()
            info[type] = i
            file_dict[stemmed_token].append(info)

            # {token1: [{p:1}, {p:5}]}

    return file_dict


def main():
    for folderName in os.listdir(os.path.join(os.getcwd(), dataPath)):
        if folderName.isdigit():
            if int(folderName) == 0: #remove in future
                print "in folder: " + folderName
                for fileName in os.listdir(os.path.join(os.getcwd(), dataPath, folderName)):
                    if fileName.isdigit():
                        if int(fileName) == 3: #remove in future
                            print "in file: " + fileName
                            with open(os.path.join(dataPath, folderName, fileName), 'r') as data_file:
                                data = data_file.read()
                                data_file.close()

                                inverted_index = dict() #for each file

                                soup = BeautifulSoup(data, "html.parser")
                                if soup.find('html') == None: #Non html files
                                    continue
                                for script in soup(["script", "style"]):
                                    script.extract()
                                # print soup.prettify()
                                extracted = element_extractor(soup, ['p'])
                                inverted_index = indexer(inverted_index, extracted, 'p')

                                if not os.path.exists(os.path.join(indexedDocumentsPath, folderName)):
                                    os.makedirs(os.path.join(indexedDocumentsPath, folderName))
                                with open(os.path.join(indexedDocumentsPath, folderName, fileName), 'wb') as indexed_doc:
                                    pickle.dump(inverted_index, indexed_doc, pickle.HIGHEST_PROTOCOL)
                                    # pickle.load(indexed_doc)

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

if __name__ == "__main__":
    main()