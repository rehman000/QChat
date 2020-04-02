from tensorflow import keras

def split_covid_data_entry(entry, word_count=255):
    """
    splits a data entry from the covid-19 text classification data set into a list of data entries where each of its
    text components are actually smaller chunks of the original texts. word_count determines the maximum amount of words 
    you want the split text to have
    """
    valid = entry['valid']
    text = entry['text']
    new_data = []
    while text != '':
        if len(text) < word_count and 0 < len(text):
            new_data.append({'text': text, 'valid': valid})
            text = ''
        else:
            new_data.append({'text': text[:word_count], 'valid': valid})
            text = text[word_count:]
    return new_data

def split_covid_data(collection, word_count=255):
    split_collection = []
    for entry in collection:
            split_collection.extend(split_covid_data_entry(entry, word_count=word_count))
    return split_collection


def word_indexer(word_lst):
    """
    takes in a list of words (i.e. strings without whitespacing and line breaks) and returns
    an encoding mapping dictionary where the key is the word and the value is its encoded integer form.
    In this encoding, 3 special keys exist:
        '<PAD>'     : 0     represents padding
        '<START>'   : 1     represents starting word
        '<UNK>'     : 2     represents uknown word
        '<UNUSED>'  : 3     represents unused word
    """
    unique_words = list(set(word_lst))
    word_index = {}
    for i in range(len(unique_words)):
        word_index[unique_words[i].lower()] = i + 4
    word_index['<PAD>'] = 0
    word_index['<START>'] = 1
    word_index['<UNK>'] = 2
    word_index['<UNUSED>'] = 3
    return word_index

def reverse_word_index(word_index):
    """
    inverts key value pair of a word index
    """
    return dict([(word_index[word], word) for word in word_index])

def listify_txt(txt):
    """
    Returns a list of words from string txt and sets all letters to be lowercase
    """
    return txt.replace(",", " , ").replace(".", " _period_ ").replace("(", " ( ").replace(")", " ) ").replace("!", " _explanation_mark_ ").replace("?", " _question_mark_ ").replace(":", " : ").replace("\"", " \" ").replace("\n", "").replace("\t", "").replace("$", "dollar_").replace("_id", "_iid").lower().strip().split(" ")

def preprocess_txt(txt, word_index, max_txt_size=255):
    """
    preprocesses a string named txt into a list of encoded integers based on word_index whose index is a word and whose value is an encoded integer
    """
    wd_list = listify_txt(txt)
    encoded = [1]
    for word in wd_list:
        if word in word_index:
            encoded.append(word_index[word])
        else:
            encoded.append(word_index["<UNK>"]) 
    encoded = keras.preprocessing.sequence.pad_sequences([encoded], value=word_index["<PAD>"], padding="post", maxlen=max_txt_size)[0]
    return encoded

