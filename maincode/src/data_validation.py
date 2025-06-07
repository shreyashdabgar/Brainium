from maincode.exceptions.exception import CustomException
from maincode.logging.logging import logging
from maincode.utills.utils import *

from sklearn.pipeline import Pipeline

from dataclasses import dataclass
import os 
import sys 
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd 

DATAVALIADAION_DIRECTORY_IN_ARTIFACTS = 'Datavalidation'

@dataclass # dataclass is used for creating and using class without __init__ mehthod 
class DataValidationconfig:
    ''' here we have to define what we want in the end of class 
            lets say we want to create pickle file for of preprocesser in end of the class
            so we will define the path of preprocesser in pickle file in this config class'''
    preprocesser_file_path : str = os.path.join('artifacts', 'preprocesser.pkl')
    train_arr_file_path  =  os.path.join('artifacts','train_arr.npy')
    test_arr_file_path = os.path.join('artifacts', 'test_arr.npy')


class Datavalidation:
    def __init__(self):
        self.datavalidationconfig = DataValidationconfig()

    def preprocesser(self):
        try:
            logging.info('feture engineering started')
            logging.info('Pipeline building for feture engineering started')
            catogerical_features = ['Geography', 'Gender']

            geogreaphy_catogary = ['France', 'Spain', 'Germany']
            gender_catogary  = ['Female', 'Male']

            catogerical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
                ('onehot', OrdinalEncoder(categories=[geogreaphy_catogary, gender_catogary])),
                ('scaler', StandardScaler())
            ])

            preprocesser = ColumnTransformer([
                ['catogary', catogerical_pipeline, catogerical_features]
            ])
            logging.info('Pipeline has build succesfully')

            return preprocesser


        except Exception as e:
            raise CustomException(e , sys)
        


    def intiate_data_validation(self, train_file_path: str , test_file_path : str): # here we are deifine the test and train pathbecuse in the end process we have to give tarin and test file which is define in data ingestion at the end 
        try:
            logging.info("Data validation is started")

            '''1 step is to read the data from the source'''

            if not os.path.exists(train_file_path and test_file_path):
                raise ValueError (' Train and Test file is not correclty found or intialized')
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            logging.info('Data is read from the its source ')

            # 2 setp is to devide the data in x train and y train and x test and y test

            if train_df is None or test_df is None:
                raise ValueError("Train and Test df is not coreectly intialixed or is empty")
            x_train = train_df.drop(columns=['Exited', 'RowNumber', 'CustomerId', 'Surname'], axis=1)
            y_train = train_df['Exited']

            x_test = test_df.drop(columns=['Exited', 'RowNumber', 'CustomerId', 'Surname'], axis=1)
            y_test = test_df['Exited']
            logging.info('Data is divided into x_train, y_train, x_test, y_test')

            '''3 step is to create the preprocesser object and fit the data in it and store in datavaliadtion config file location'''
            preprocesser_obj = self.preprocesser()

            save_obj(
                obj= preprocesser_obj,
                file_path=self.datavalidationconfig.preprocesser_file_path
            )

            x_train_preccesd  = preprocesser_obj.fit_transform(x_train)
            x_test_proccesd  = preprocesser_obj.transform(x_test)

            # we doesnt use fit transform for y_train and y_test becuase it is already in 0 and 1 so dont need it and yeah it is help to secure data leakage
            # now we combine x _train and y_train togather

            logging.info('Combining x_train and x_test with y_train and y_test')
            train_arry = np.column_stack((x_train_preccesd, np.array(y_train)))
            test_arry = np.column_stack((x_test_proccesd, np.array(y_test)))
            #created numpy array and save in the loacation of datavalidation config 
            np.save(self.datavalidationconfig.train_arr_file_path, train_arry)
            np.save(self.datavalidationconfig.test_arr_file_path, test_arry)


            ''' return is decide based on some factors like what is use of in next file what is logic in this current function
            like ex. in dataingestion return is file path insted of file becuase we use file path i starting in this function'''

            logging.info('Data validation is done')

            return(  
                train_arry, 
                test_arry, 
                self.datavalidationconfig.preprocesser_file_path

            )


        except Exception as e :
            raise CustomException(e, sys)