import os 
import sys 

from maincode.exceptions.exception import CustomException
from maincode.logging.logging import logging
from maincode.utills.utils import read_data

from sklearn.model_selection import train_test_split
import pandas as pd

from dataclasses import dataclass



@dataclass # here we use dataclass becuse we dont want to write a constructor(__init__) for this class 
class Dataingtestionconfig():
    train_file_path :str = os.path.join('artifacts', 'train.csv')
    test_file_path :str  = os.path.join('artifacts', 'test.csv')
    data_file_path :str = os.path.join('artifacts', 'data.csv')

class Dataingestion:

    def __init__(self):
        self.dataingestioconfig = Dataingtestionconfig()

    def intiate_data_ingestion(self):
        try:
            logging.info('Data ingestion is Start')
            '''1 step is to read the data from the source'''
            df = pd.read_csv('Churn_Modelling.csv')

            '''storing the data in the artifacts folder'''
            if df.empty:
                raise ValueError(f"{df} is empty")
            
            os.makedirs(os.path.dirname(self.dataingestioconfig.data_file_path), exist_ok=True)

            df.to_csv(self.dataingestioconfig.data_file_path, index = False, header = True)
            
            ''' 2 setp is to split te data into trainb and test data'''

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            '''3 step is to save the train and test data in the artifacts folder'''
            if not os.path.exists(os.path.dirname(self.dataingestioconfig.train_file_path)):
                os.makedirs(os.path.dirname(self.dataingestioconfig.train_file_path), exist_ok=True)

            logging.info('Train and Test data is cerated and save in the artifacts folder')
            train_set.to_csv(self.dataingestioconfig.train_file_path, index=False, header=True)
            test_set.to_csv(self.dataingestioconfig.test_file_path, index=False, header=True)

            return(
                self.dataingestioconfig.train_file_path,
                self.dataingestioconfig.test_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)