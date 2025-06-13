from maincode.exceptions.exception import CustomException
from maincode.logging.logging import logging
from maincode.utills.utils import *

import os 
import sys 

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from datetime import datetime
from dataclasses import dataclass

@dataclass 
class ModelEvalutionConfig:
    '''this class take trained model pickle file'''
    trained_model_pickle_file = os.path.join('artifacts' , 'AnnModel.h5' )

class ModelEvalution:
    def __init__(self):
        #object creation for model_evelution
        self.model_config = ModelEvalutionConfig()

    def intiate_model_evelution(self, train_arr , test_arr):# we take parameter train_arr and test_arr becuase train and test arr is needed for model evelution or model_training or creation
        try :
            logging.info('Model Evelution is Started')
            x_train = train_arr[:, :-1]# take all rows and take columns except 
            y_train = train_arr[:, -1]
            x_test = test_arr[:, :-1]
            y_test = test_arr[: , -1]

            '''Defing the Model'''
            model = Sequential([
                Dense(64 ,activation ='relu', input_shape=(x_train.shape[1],)),#creating first hidden layer which is connected with input layer
                Dense(32,activation ='relu' ),## creating second hidden layer
                Dense(1,activation = 'sigmoid')## creating output layer

            ])
            ''' Doing froward and Backward propgation'''
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            '''setup the tensorboard'''
            logging.info('tensorboard startup')
            tensorboard_callback = TensorBoard(log_dir='logs/tensorboard', histogram_freq=1)

            # Early stopping (it stops epochs when the loss value stops decreasing)
            early_stopping_callback = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            print(early_stopping_callback)

            logging.info('Model Training is start')
            # Fit the model using the callbacks
            model.fit(
                x_train, y_train,
                validation_data=(x_test, y_test),
                epochs=100,
                callbacks=[tensorboard_callback, early_stopping_callback]
            )

            model.save(self.model_config.trained_model_pickle_file)
            

            return(self.model_config.trained_model_pickle_file)
            
        except Exception as e :
            raise CustomException(e, sys)
