import os 
import sys 
from maincode.src.data_ingestion import Dataingestion
from maincode.src.data_validation import Datavalidation
from maincode.src.ANN_model_evulution import ModelEvalution
from maincode.exceptions.exception import CustomException
from maincode.logging.logging import logging

if __name__ == "__main__":
    try:
        logging.info("data ingestion exicution is started")
        dataingestion = Dataingestion()
        train_path , test_path  = dataingestion.intiate_data_ingestion()
        logging.info("data ingestion excution is completed")
        print(f"Train path: {train_path}")
        print(f"Test path: {test_path}")

        logging.info('Datavaliadtion execution precess is Started')
        data_validation = Datavalidation()
        train_arry , test_arry , pickle_file_path =data_validation.intiate_data_validation(train_file_path=train_path, test_file_path=test_path)
        logging.info('Datavalidation execution is Completed')

        logging.info('Model Training is Start')
        ModelTrainer = ModelEvalution()
        pickle_file = ModelTrainer.intiate_model_evelution(train_arr=train_arry, test_arr=test_arry)
        logging.info('Model Training is Done')


    except Exception as e :
        raise CustomException(e, sys)