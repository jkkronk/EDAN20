import regex as re
import pickle
import os
import math
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

word_dict = dict()
dict_dict = dict()
master_dict = dict()
corpus = dict()
word_count = dict()


def text_cleaner(text):
    """
    :param str text: File to be cleaned up. The function will remove all non letter characters and make all letters
    lower case
    :return str text: the new text file
    """
    # Removes all new lines and replaces with spaces.
    text = re.sub("\n", " ", text)
    # Replace non-letters with space
    text = re.sub('\P{L}', ' ', text) # [^a-zöäåA-ZÖÄÅ\s]

    # Make all words lower case
    text = text.lower()
    return text


def word_indexer(text):
    """
    Indexes all the words in the text, and appends them to the global dictionay word_dict.
    :param str text: the string which should be indexed.
    """
    # Match every word in string text.

    for match in re.finditer(r'\p{L}+', text.lower()):
        match_word = match.group()
        # If the word exist in the dict, append the new index.
        if match_word in word_dict.keys():
            word_dict[match_word].append(match.start(0))
        # If the word does not yet exist as a key. Add it with its index for the first time, as a list.
        else:
            word_dict[match_word] = [match.start(0)]
    return word_dict


def build_dict(text):
    """
    Adds words to global dictionary 'corpus'
    :param str text: all words in the string text will be added to a dictionary. String text must be letters only and
    all lower case.
    """
    global corpus
    text = text_cleaner(text)
    for word in text.split(' '):
        corpus[word] = []

def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    :param dir: The directory of the files
    :param suffix: The suffix the files end in. Example '.txt'.
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

def reset_dict():
    """
    Resets the dictionary word_dict. Used for when storing word_dict into dict_dict.
    """
    global word_dict
    word_dict = dict()

def tf_idf2(files):
    """
    Calculates the tf idf for the gives files.
    :param files:
    :return: dict tf_dict:
    """
    n = 9
    global word_count
    tf_dict = dict()
    df = 0
    for file_name in files:  # In each file, how many times do the word occur
        tf_dict[file_name] = dict()
        for word in master_dict:
            df = len(master_dict[word]) # In how many stories does the word occur
            try:
                tf = len(master_dict[word][file_name])
            except:
                nop = 1
            if df != 0:
                weigh = math.log10(9/df)*tf/word_count[file_name]
                tf_dict[file_name][word] = weigh
                df = 0
                tf = 0
    return tf_dict



def master_indexer():
    """
    Indexes all words to which textfile they occur in, and at which index.
    {word: {file_name: [start0, start1, ...]}} to file master_dict.
    :return:
    """
    global master_dict
    global corpus
    for word in corpus:
        master_dict[word] = {}
        for file_name in files:
            try:
                master_dict[word][file_name] = dict_dict[file_name][word]
            except:
                nop = 1

def build_matrix(tf_dict):
    """

    :param tf_dict: dictionary with {file_name: {word : tf-value}}
    :return:
    """
    doc_matrix = np.zeros((9,len(corpus.keys())))
    word_list = corpus.keys()
    file_list = dict_dict.keys()
    for i, word in enumerate(word_list):
        for j, file in enumerate(file_list):
            try:
                doc_matrix[j, i] =tf_dict[file][word]# tf_dict[file][word]
                #print(doc_matrix[j, i], 'hej', tf_dict[file][word])
            except:
                #print('didnt work')
                nop = 1
    df = pd.DataFrame(doc_matrix)
    similarity_matrix = cosine_similarity(df)

    temp_matrix = similarity_matrix

    for i, row in enumerate(temp_matrix):
        row[i] = 0
    max_tal = np.amax(temp_matrix)
    result = np.where(temp_matrix == np.amax(temp_matrix))
    print(result)

    for i in range(0,9):
        temp_matrix[i,i] = 0
    print(np.amax(similarity_matrix))


if __name__ == "__main__":
    #tf_dict = dict()
    #global dict_dict
    files = get_files('Selma2', 'txt')

    for file_name in files:

        fil = open('Selma2/'+file_name, 'r')
        fil = fil.read()

        #fil = text_cleaner(filen)
        word_count[file_name]= len(fil.split(" "))


        word_dict = word_indexer(fil)
        build_dict(fil)
        # pickle.dump(word_dict, open('{}.idx'.format(file_name), 'wb'))
        # Building master index:
        dict_dict[file_name] = word_dict

        # Reset the word_dict so it can store new text file
        reset_dict()
    master_indexer()
    print(corpus)
    #print(master_dict['samlar'])
    tc_dict = tf_idf2(files)
    #print(tc_dict)
    #print(tc_dict['bannlyst.txt']['et'])
    build_matrix(tc_dict)
    # for i in corpus:
    #     print(i)
