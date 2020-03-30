from app.machine_learning import covid19 
import os

def check_if_covid19_works(method):
    """
    testing to see if the library is functional
    """
    if method == 'json':
        covid19.json_train()
        file_dir = os.path.dirname(os.path.abspath(__file__))
        word_index_filepath = os.path.join(file_dir, 'data', 'word_decode.json')
        txt = input()
        res = covid19.validate_txt(txt, use_json=True)
    elif method == 'mongo':
        covid19.mongo_train()
        txt = input()
        res = covid19.validate_txt(txt, use_json=False)
    else:
        res = 'invalid data storage method ' + method
    print(res)