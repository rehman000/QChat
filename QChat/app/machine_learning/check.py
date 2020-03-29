from app.machine_learning import covid19 
import os

def check_if_covid19_works():
    """
    testing to see if the library is functional
    """
    covid19.json_train()
    file_dir = os.path.dirname(os.path.abspath(__file__))
    word_index_filepath = os.path.join(file_dir, 'dummy_word_decode.json')
    txt = input()
    res = covid19.validate_txt_json(txt, word_index_filepath)
    print(res)