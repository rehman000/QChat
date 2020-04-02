from app import mongo
import json
from app.machine_learning.data.process import split_covid_data_entry, split_covid_data


def traindata_json_to_mongo(filepath='text_data.json', splice=False):
    with open(filepath) as f:
        train_data = json.load(f)
    mongo_data = []
    if splice:
        mongo_data = split_covid_data(train_data)
    else:
        mongo_data = train_data
    mongo.db.traindata.drop()
    mongo.db.traindata.insert_many(mongo_data)

    with mongo.db.traindata.find({}, {"_id": 0, "text": 1, "valid": 1}) as c:
        trainingdata = list(c)

    print(f'You have stored {len(trainingdata)} data points for your training data')