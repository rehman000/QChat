import tensorflow as tf
from tensorflow import keras

def validate_covid19(txt):
    """
    Takes in text and returns an integer determining if a text provides valid information 
    or misinformation about the COVID-19 virus.
    If a text is valid, then the function returns 2.
    If a text is neither valid nor misinformation, returns 1.
    If a text is misinformation, returns 0
    """
    return 1