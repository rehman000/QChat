import tensorflow as tf
from tensorflow import keras
import json
from app import mongo
import numpy as np
import os
from app.machine_learning.data.process import preprocess_txt, listify_txt, word_indexer, split_covid_data_entry, split_covid_data


def preprocess_covid19_data(collection, max_txt_size=255, splice=True):
    """
    Takes in a list of dictionaries where each dictionary takes the form:
    {
        'text': a string block,
        'valid': an integer
    }
    and max_txt_size which will set the size of your texts in collection to that size.
    It will return a list of encoded texts, a list of valid labels, and a word_index that maps a word to an encoded integer form
    """
    if splice:
        collection = split_covid_data(collection)
    np.random.shuffle(collection)
    labels = np.array([data['valid'] for data in collection], dtype=np.int32)
    texts =  [data['text'] for data in collection]
    word_dump = []
    for text in texts:
        word_dump.extend(listify_txt(text))
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
    model.add(keras.layers.Dense(64,activation="relu"))
    model.add(keras.layers.Dense(16,activation="relu"))
    model.add(keras.layers.Dense(3,activation="softmax"))

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=validation_data, verbose=1)
    return model

def train_save_info_validator(x_train, y_train, embeding_dim=(88000,16), epochs=7, batch_size=None, validation_data=None):
    """
    trains neural network with training data and saves it
    """
    if validation_data == None:
        print('no validation data added')
        model = train_info_validator(x_train, y_train, embeding_dim=embeding_dim, epochs=epochs, batch_size=batch_size, validation_data=validation_data)
    else:
        max_accuracy = 0
        average_accuracy = 0
        model = None
        for i in range(10):
            print(f'Beggining to train the {i+1}th model')
            new_model = train_info_validator(x_train, y_train, embeding_dim=embeding_dim, epochs=epochs, batch_size=batch_size, validation_data=validation_data)
            accuracy = new_model.evaluate(validation_data[0], validation_data[1])[1]
            print(f'Finished training {i+1}th model with validation accuracy {accuracy}')

            average_accuracy = (i*average_accuracy + accuracy)/(i+1)
            if accuracy > max_accuracy:
                model = new_model
                max_accuracy = accuracy
                print(f'More accurate model chosen.\nChosen model\'s validation Accuracy: {max_accuracy}')
            else:
                print('Model not accurate enough, model discarded ... ')
        print(f'the average accuracy of all models is {average_accuracy}')
        print(f'Will now save model with validation accuracy: {max_accuracy}')
    file_dir = os.path.dirname(os.path.abspath(__file__))
    model.save(os.path.join(file_dir, "covid19_info_validator.h5"))
    return model

def json_train(data_filepath=None, word_index_filename=None, splice=True):
    """
    trains neural network from a json data
    """
    file_dir = os.path.dirname(os.path.abspath(__file__))
    if data_filepath == None:        
        data_filepath = os.path.join(file_dir, 'data', 'text_data.json')

    if word_index_filename == None:
        word_index_filename = os.path.join(file_dir, 'data', 'word_decode.json')

    with open(data_filepath) as f: 
        training_collection = json.load(f) # get training collection

    train_size = len(training_collection) - len(training_collection)//5

    x_train, y_train, word_index = preprocess_covid19_data(training_collection, splice=splice) # preprocess training collection
    x_train, y_train, x_val, y_val = x_train[:train_size], y_train[:train_size], x_train[train_size:], y_train[train_size:]

    with open(word_index_filename, 'w') as f:
        json.dump(word_index, f) # store word index

    model = train_save_info_validator(x_train, y_train, embeding_dim=(len(word_index), 16), epochs=20, validation_data=(x_val, y_val))

def mongo_train(splice=True):
    """
    trains neural network using mongodb data
    """
    with mongo.db.traindata.find({}, {"_id": 0, "text": 1, "valid": 1}) as c:
        training_collection = list(c)
    train_size = len(training_collection) - len(training_collection)//5

    x_train, y_train, word_index = preprocess_covid19_data(training_collection, splice=splice) # preprocess training collection
    x_train, y_train, x_val, y_val = x_train[:train_size], y_train[:train_size], x_train[train_size:], y_train[train_size:]

    mongo.db.wordindex.drop()
    mongo.db.wordindex.insert_one(word_index)
    model = train_save_info_validator(x_train, y_train, embeding_dim=(len(word_index), 32), epochs=20, validation_data=(x_val, y_val))

def validate_txt_with_index(txt, word_index, model=None):
    """
    Takes in text and an encoding word index and returns an integer determining if a text provides valid information 
    or misinformation about the COVID-19 virus.
    If a text is valid, then the function returns 0.
    If a text is neither valid nor misinformation, returns 1.
    If a text is misinformation, returns 2

    You can also optionally pass a model which represents a keras neural network instead of the function loading
    a pre-existing neural network
    """
    if not model:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        model = keras.models.load_model(os.path.join(file_dir, "covid19_info_validator.h5"))
        
    encoded = preprocess_txt(txt, word_index=word_index)
    prediction = model.predict(np.array([encoded], dtype=np.int32))[0] # a numoy of int33 datatype is only permitted
    return np.argmax(prediction)    

def validate_txt_json(txt, word_index_filepath=None, model=None):
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
    if word_index_filepath==None:
        word_index_filepath = os.path.join(file_dir, 'data' + os.sep + 'word_decode.json')
    with open(word_index_filepath) as f:
        word_index = json.load(f)
    return validate_txt_with_index(txt, word_index, model=model)

def validate_txt_mongo(txt, model=None):
    """
    To be used if your data is stored in a mongodb database
    Takes in text and returns an integer determining if a text provides valid information 
    or misinformation about the COVID-19 virus.
    If a text is valid, then the function returns 0.
    If a text is neither valid nor misinformation, returns 1.
    If a text is misinformation, returns 2

    You can also optionally pass a model which represents a keras neural network instead of the function loading
    a pre-existing neural network.
    """
    word_index = mongo.db.wordindex.find_one()
    return validate_txt_with_index(txt, word_index, model=model)

def validate_txt(txt, use_json=False, model=False):
    """
    Takes in text and returns an integer determining if a text provides valid information 
    or misinformation about the COVID-19 virus.
    If a text is valid, then the function returns 0.
    If a text is neither valid nor misinformation, returns 1.
    If a text is misinformation, returns 2

    By default the app validates information using data from mongodb but you can set use_json to True to use json data.

    You can also optionally pass a model which represents a keras neural network instead of the function loading
    a pre-existing neural network
    """
    if use_json:
        return validate_txt_json(txt, model=model)
    else:
        return validate_txt_mongo(txt, model=model)