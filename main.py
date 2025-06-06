import os 
import sys 
from maincode.src.data_ingestion import Dataingestion
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

    except Exception as e :
        raise CustomException(e)