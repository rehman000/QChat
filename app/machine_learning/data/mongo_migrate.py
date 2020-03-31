from app import mongo
import json

def split_data(entry, word_count=255):
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


def traindata_json_to_mongo(filepath='text_data.json', splice=False):
    with open(filepath) as f:
        train_data = json.load(f)
    mongo_data = []
    for entry in train_data:
        if splice:
            spliced_data = split_data(entry)
            mongo_data.extend(spliced_data)
        else:
            mongo_data.append(entry)
    mongo.db.traindata.drop()
    mongo.db.traindata.insert_many(mongo_data)

    trainingdata = list(mongo.db.traindata.find({}, {"_id": 0, "text": 1, "valid": 1}))
    # for data in trainingdata:
    #     print(data)
    print(f'You have stored {len(trainingdata)} data points for your training data')