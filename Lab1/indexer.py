import re

word_dict = dict()


def text_cleaner(text):
    """
    :param str text: File to be cleaned up. The function will remove all non letter characters and make all letters lower
    case
    :return str text: the new text file
    """
    # Removes all new lines and replaces with spaces.
    text = re.sub("\n", " ", text)
    # Replace non-letters with nothing
    text = re.sub("[^a-zåäöA-ZÅÄÖ0-9 ]", '', text)
    # Make all words lower case
    text = text.lower()
    return text


def word_indexer(text):
    """
    Indexes all the words in the text, and appends them to the global dictionay word_dict.
    :param str text: the string which should be indexed.
    """
    global word_dict
    text_size = len(text)
    index = 0
    word = ''
    print(text)
    for char in text:
        if char != ' ':
            word = word + char
        elif char == ' ':
            word_dict[word].append(index - len(word))
            #word_dict[word] = [word_dict[word], index - len(word)]
            print(word, word_dict[word])
            word = ''
        index = index + 1
    # for match in re.finditer('detta', text):
    #     print(match)
    #     # print(match.groups(0))
#



def word_indexer2(text):
    """
    Indexes all the words in the text, and appends them to the global dictionay word_dict.
    :param str text: the string which should be indexed.
    """
    global word_dict
    #text_size = len(text)
    #index = 0
    word = ''
    # Match every word in string text
    for match in re.finditer(r'\b[a-zöäå]+\b', text):
        #print(match.group(), '# first line')
        #print(match.start(0))
        match_word = match.group()
        # If the word exist in the dict, append the new index.
        if match_word in word_dict.keys():
            word_dict[match_word].append(match.start(0))
        # If the word does not yet exist at a key. Add it with its index for the first time, as a list.
        else:
            word_dict[match_word] = [match.start(0)]





def build_dict(text):
    """
    Adds words to global dictionary 'word_dict'

    :param str text: all words in the string text will be added to a dictionary. String text must be letters only and
    all lower case.
    """
    global word_dict
    for word in text.split(' '):
        word_dict[word] = []


if __name__ == "__main__":
    file = open("Selma/conct_file.txt", 'r')
    #file = open("test_file.txt", 'r')
    file = file.read()
    file = text_cleaner(file)
    #build_dict(file)

    word_indexer2(file)
    for key in word_dict:
        print(key, word_dict[key])
    #print(word_dict, '# print from main')
    print('och', word_dict['och'])
    print(len(file),'längden av texten')
    #TODO : Question: Why do we have to use finditer. It would be better if we could simply iterate through the text
    # find words, and append with corresponding index. Instead now we must first build dict, and later iterate again
