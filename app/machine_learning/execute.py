from app.machine_learning import train, check
from app.machine_learning.data.mongo_migrate import traindata_json_to_mongo
from app.machine_learning.data.analyze import json_covid_valid_freq, mongo_covid_valid_freq
import os

def print_help():
    print('\n\npython run.py ml <action>\n')
    print('Actions:\n') 
    print('\ttrain: trains a specific machine learning AI \n\t\tpython run.py ml train <AI> <storage method> [option]')
    print('\tcheck: tests a machine learning AI to see if it is functional\n\t\tpython run.py ml check <AI> <storage method>')
    print('\tdata: manage trainibg data\n\t\tpython run.py ml data <data_method> [option]')
    print('\t\tdata methods:')
    print('\t\t\tjson_mongo: sends json training data to a mongo database')
    print('\t\t\t\tpython run.py ml data json_mongo [option]')
    print('\t\t\tcovid_freq: Checks frequency of validity values of the covid19 text validator\'s training data')
    print('\t\t\t\tpython run.py ml data covid_freq <storage method>')
    print('\t help: show help')
    print('AI:') 
    print('\tcovid19: a neural network that checks if a piece of text has verified info on covid-19, misinformation, or neither')
    print('storage methods:') 
    print('\tjson: data is stored using json')
    print('\tmongo: data is stored using mongodb')
    print('options:') 
    print('\t splice: splice data if they are in a text form')

def execute(args):
    if len(args) == 0:
        print_help()
    elif args[0] == 'check':
        if args[1] == 'covid19':
            if len(args) > 2:    
                check.check_if_covid19_works(args[2])
            else:
                check.check_if_covid19_works('')
        else:
            print('error: you must type a valid AI')
    elif args[0] == 'train':
        if args[1] == 'covid19':
            if len(args) > 3:
                    splice = args[3]
            else:
                splice = None
            if len(args) > 2:
                train.train_covid19(args[2], splice=splice)
            else:
                train.train_covid19('')
        else:
            print('error: you must type a valid AI')
    elif args[0] == 'data':
        if args[1] == 'json_mongo':
            filepath = os.path.join(os.path.dirname(__file__), 'data', 'text_data.json')
            splice = False
            if len(args) > 2:
                splice=args[2]=='splice'
            traindata_json_to_mongo(filepath=filepath, splice=splice)
        if args[1] == 'covid_freq':
            print('Checking frequency of validity values of the covid19 text validator\'s training data')
            print('Key: 0 == valid, 2 == neutral, 2 == misinformation')
            if args[2] == 'json':
                print(json_covid_valid_freq())
            elif args[2] == 'mongo':
                print(mongo_covid_valid_freq())
            else:
                print('you must input a valid storage method')
    elif args[0] == 'help':
        print_help()
    else:
        print('error: you must input a valid machine learning action')