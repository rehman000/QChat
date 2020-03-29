import tensorflow as tf
from tensorflow import keras
import json
# from app import mongo
from flask import Flask
import numpy as np
import os

def word_indexer(word_lst: list):
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
    return dict([(word_index[word], word) for word in word_index])

def clean_txt(txt):
    """
    Returns a list of words from string txt that removes unneeded characters and sets them all to be lowercases
    """
    return txt.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"", "").replace("\n", "").replace("\t", "").lower().strip().split(" ")

def preprocess_txt(txt, word_index, max_txt_size=250):
    """
    preprocesses a string named txt into a list of encoded integers based on word_index whose index is a word and whose value is an encoded integer
    """
    wd_list = clean_txt(txt)
    encoded = [1]
    for word in wd_list:
        if word in word_index:
            encoded.append(word_index[word])
        else:
            encoded.append(word_index["<UNK>"]) 
    encoded = keras.preprocessing.sequence.pad_sequences([encoded], value=word_index["<PAD>"], padding="post", maxlen=max_txt_size)[0]
    return encoded


def preprocess_training_collection(collection, max_txt_size=250):
    """
    Takes in a list of dictionaries where each dictionary takes the form:
    {
        'text': a string block,
        'valid': an integer
    }
    and max_txt_size which will set the size of your texts in collection to that size.
    It will return a list of encoded texts, a list of valid labels, and a word_index that maps a word to an encoded integer form
    """
    labels = np.array([data['valid'] for data in collection], dtype=np.int32)
    texts =  [data['text'] for data in collection]
    word_dump = []
    for text in texts:
        word_dump.extend(clean_txt(text))
    word_index = word_indexer(word_dump)
    del word_dump
    encoded_txt = np.array([preprocess_txt(text, word_index, max_txt_size) for text in texts])
    return encoded_txt, labels, word_index

def train_info_validator(x_train, y_train, embeding_dim=(88000,16), epochs=7, batch_size=None, validation_data=None):
    """
    trains neural network with training data
    """
    model = keras.Sequential()
    model.add(keras.layers.Embedding(embeding_dim[0],embeding_dim[1]))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16,activation="relu"))
    model.add(keras.layers.Dense(3,activation="softmax"))

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=validation_data, verbose=1)
    return model

def train_save_info_validator(x_train, y_train, embeding_dim=(88000,16), epochs=7, batch_size=None, validation_data=None):
    """
    trains neural network with training data and saves it
    """
    model = train_info_validator(x_train, y_train, embeding_dim=embeding_dim, epochs=epochs, batch_size=batch_size, validation_data=validation_data)
    file_dir = os.path.dirname(os.path.abspath(__file__))
    model.save(os.path.join(file_dir, "covid19_info_validator.h5"))
    return model

def validate_txt(txt, word_index, model=None):
    """
    Takes in text and an encoding word index and returns an integer determining if a text provides valid information 
    or misinformation about the COVID-19 virus.
    If a text is valid, then the function returns 0.
    If a text is neither valid nor misinformation, returns 1.
    If a text is misinformation, returns 2

    You can also optionally pass a model which represents a keras neural network instead of the function loading
    a pre-existing neural network
    """
    if model==None:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        model = keras.models.load_model(os.path.join(file_dir, "covid19_info_validator.h5"))

    encoded = preprocess_txt(txt, word_index=word_index)
    prediction = model.predict(np.array([encoded], dtype=np.int32))[0] # a numoy of int33 datatype is only permitted
    return np.argmax(prediction)

def validate_txt_json(txt, word_index_filename=None, model=None):
    """
    Takes in text and the filename of word index json file and returns an integer determining if a text provides valid information 
    or misinformation about the COVID-19 virus.
    If a text is valid, then the function returns 0.
    If a text is neither valid nor misinformation, returns 1.
    If a text is misinformation, returns 2

    You can also optionally pass a model which represents a keras neural network instead of the function loading
    a pre-existing neural network
    """
    file_dir = os.path.dirname(os.path.abspath(__file__))
    if word_index_filename==None:
        word_index_filename = 'dummy_word_decode.json'
    with open(os.path.join(file_dir, word_index_filename)) as f:
        word_index = json.load(f)
    return validate_txt(txt, word_index, model=model)
        
    

def json_train(data_filepath=None, word_index_filename='dummy_word_decode.json'):
    """
    trains neural network from a json data
    """
    if data_filepath == None:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        data_filepath = os.path.join(file_dir, 'dummy_text_data.json')

    with open(data_filepath) as f: 
        training_collection = json.load(f) # get training collection

    x_train, y_train, word_index = preprocess_training_collection(training_collection) # preprocess training collection

    with open(os.path.join(file_dir, word_index_filename), 'w') as f:
        json.dump(word_index, f) # store word index

    model = train_save_info_validator(x_train, y_train, embeding_dim=(len(word_index), 16), epochs=40)

def mongo_train():
    """
    trains neural network using mongodb data
    """
    pass

if __name__ == '__main__':
    """
    testing to see if the library is functional
    """
    json_train()
    file_dir = os.path.dirname(os.path.abspath(__file__))
    word_index_filepath = os.path.join(file_dir, 'dummy_word_decode.json')
    txt = input()
    res = validate_txt_json(txt, word_index_filepath)
    print(res)