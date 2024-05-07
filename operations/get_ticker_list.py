from queue import *
import logging
import os 
import pandas as pd 
import glob
from flask import json

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
ticker_list_log_name = os.path.join(log_dir, 'ticker_list.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data\\raw_data')

logging.basicConfig(filename=ticker_list_log_name, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def get_ticker_list():
    file_list = []
    csv_files = [file for file in glob.glob(csv_dir + '\\*', recursive=False) if not os.path.isdir(file)]
    
    for file in csv_files:
        separator = 'raw_data\\'
        target_file = file.split(separator, 1)[1]
        separator = '.csv'
        target_file = target_file.split(separator, 1)[0]
        logging.info("Target file to append: %s" %target_file)
        file_list.append(target_file)
    return json.dumps(file_list)