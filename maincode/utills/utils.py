'''here we write all kind of utility function(genral function ) which is need in our project'''
# basically we write genral funcion here which is use most of the time in project 

import os 
import sys 
from maincode.exceptions.exception import CustomException
from maincode.logging.logging import logging
import pandas as pd
import pickle
def read_data(file_path : str):
    try:
        df = pd.read_csv(file_path) # we give here a file path becuse this is genric function and data is store on file path
    except Exception as e:
        raise CustomException(e)
    

def save_obj(file_path : str, obj : object):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)