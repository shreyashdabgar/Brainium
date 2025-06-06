import os 
import logging 
import sys
from datetime import datetime


# Generate a log file becuase we put there .log name based on the current date in the format 'YYYY-MM-DD.log' and store it in the LOG_FILE variable
LOG_FILE = datetime.now().strftime('%Y-%m-%d') + '.log' 

#creatig a coustem logger directory
log_path = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(log_path):
    os.makedirs(log_path)
else :
    print(f"Directory {log_path} already exists.")

#cerating logging file path inside the directory
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d',
    level=logging.INFO
)


