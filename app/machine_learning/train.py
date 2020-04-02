from app.machine_learning import covid19 

def train_covid19(method, splice=None):
    """
    takes a string ai which determines which AI is trained and method which determines how it is trained
    """
    if splice == 'splice':
        splice = True
    else:
        splice = False

    if method == 'json':
        covid19.json_train(splice=splice)
    elif method == 'mongo':
        covid19.mongo_train(splice=splice)
    else:
        print('invalid training method')
