from app.machine_learning import covid19 

def train_covid19(method):
    """
    takes a string ai which determines which AI is trained and method which determines how it is trained
    """
    if method == 'json':
        covid19.json_train()
    else:
        covid19.mongo_train()
