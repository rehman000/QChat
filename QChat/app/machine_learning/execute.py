from app.machine_learning import train, check
from app.machine_learning.data.mongo_migrate import traindata_json_to_mongo
import os

def print_help():
    print('\n\npython run.py ml action\n')
    print('Actions:\n') 
    print('\t train: trains a specific machine learning AI \n\n\t\tpython run.py ml train <AI> <storage method>\n')
    print('\t check: tests a machine learning AI to see if it is functional\n\n\t\tpython run.py ml check <AI> <storage method>\n')
    print('\t data: manage trainibg data\n\n\t\tpython run.py ml data <data_method> [option]\n')
    print('\t\tdata methods:\n\n\t\t\t json_mango: sends json training data to a mongo database\n')
    print('\t\toptions:\n\n\t\t\t splice: splice training data if they are in a text form\n')
    print('\t help: show help\n')
    print('AI:\n') 
    print('\t covid19: a neural network that checks if a piece of text has verified info on covid-19, misinformation, or neither\n')
    print('storage methods:\n') 
    print('\t json: data is stored using json\n')
    print('\t mongo: data is stored using mongodb\n')

def execute(*args):
    args = args[0]
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
            if len(args) > 2:
                train.train_covid19(args[2])
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
    elif args[0] == 'help':
        print_help()
    else:
        print('error: you must input a valid machine learning action')