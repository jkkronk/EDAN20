"""
Baseline chunker for CoNLL 2000
"""
__author__ = "Pierre Nugues"

import conll_reader


def count_pos(corpus):
    """
    Computes the part-of-speech distribution
    in a CoNLL 2000 file
    :param corpus:
    :return:
    """
    pos_cnt = {}
    for sentence in corpus:
        for row in sentence:
            if row['pos'] in pos_cnt:
                pos_cnt[row['pos']] += 1
            else:
                pos_cnt[row['pos']] = 1
    return pos_cnt


def train(corpus):
    """
    Computes the chunk distribution by pos
    The result is stored in a dictionary
    :param corpus:
    :return:
    """

    """
    Fill in code to compute the chunk distribution for each part of speech
    """
    pos_cnt = count_pos(corpus)
    # We compute the chunk distribution by POS
    chunk_dist = {key: {} for key in pos_cnt.keys()}
    chunk_len = len(chunk_dist.keys())

    #print(pos_cnt)

    # Hur många gånger finns tex NN för varje chunk
    for sentence in corpus:
        for row in sentence:
            #print(row['pos'])
            if row == {}:
                continue
            if row['chunk'] in chunk_dist[row['pos']]:
                chunk_dist[row['pos']][row['chunk']] += 1
            else:
                chunk_dist[row['pos']][row['chunk']] = 1


    # Exempel på sidan
    print(chunk_dist['JJR'])
    # {'B-NP': 382, 'B-ADJP': 111, 'I-ADJP': 45, 'B-ADVP': 63, 'I-ADVP': 17, 'B-VP': 2, 'I-NP': 204, 'I-VP': 11, 'O': 16, 'B-PP': 2}

    """

    weigh = 0
    for count in pos_cnt:
        weigh = weigh + pos_cnt[count]

    # Calc % occurences of each part
    for chunk in chunk_dist:
        chunk_dist[chunk] = pos_cnt[chunk] / weigh

    """


    # We determine the best association
    pos_chunk = {}
    """
    Fill in code so that for each part of speech, you select the most frequent chunk.
    You will build a dictionary with key values:
    pos_chunk[pos] = most frequent chunk for pos
    """
    pos_chunk = {key: '' for key in pos_cnt.keys()}

    for pos in chunk_dist:
        max_value = 0
        max_chunk = ''
        for chunk in chunk_dist[pos]:
            #print(chunk_dist[pos][chunk], 'dawdawda')
            value = chunk_dist[pos][chunk]
            if value > max_value:
                max_value = value
                max_chunk = chunk
        pos_chunk[pos] = max_chunk
    return pos_chunk


def predict(model, corpus):
    """
    Predicts the chunk from the part of speech
    Adds a pchunk column
    :param model:
    :param corpus:
    :return:
    """
    """
    We add a predicted chunk column: pchunk
    """
    for sentence in corpus:
        for row in sentence:
            row['pchunk'] = model[row['pos']]
    return corpus


def eval(predicted):
    """
    Evaluates the predicted chunk accuracy
    :param predicted:
    :return:
    """
    word_cnt = 0
    correct = 0
    for sentence in predicted:
        for row in sentence:
            word_cnt += 1
            if row['chunk'] == row['pchunk']:
                correct += 1
    return correct / word_cnt


if __name__ == '__main__':
    column_names = ['form', 'pos', 'chunk']
    train_file = 'train.txt' #'../../corpus/conll2000/train.txt'
    test_file = 'test.txt'#'../../corpus/conll2000/test.txt'

    train_corpus = conll_reader.read_sentences(train_file)
    train_corpus = conll_reader.split_rows(train_corpus, column_names)
    test_corpus = conll_reader.read_sentences(test_file)
    test_corpus = conll_reader.split_rows(test_corpus, column_names)

    model = train(train_corpus)

    # Exemepl från sidan
    print(model['NN'], 'hej')
    predicted = predict(model, test_corpus)
    accuracy = eval(predicted)
    print("Accuracy", accuracy)
    f_out = open('out', 'w')
    # We write the word (form), part of speech (pos),
    # gold-standard chunk (chunk), and predicted chunk (pchunk)
    for sentence in predicted:
        for row in sentence:
            f_out.write(row['form'] + ' ' + row['pos'] + ' ' +
                        row['chunk'] + ' ' + row['pchunk'] + '\n')
        f_out.write('\n')
    f_out.close()