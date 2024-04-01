from dateutil.relativedelta import relativedelta
from queue import *
import pandas as pd 
import logging
import glob
import os 
from flask import json


dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
gather_data_log_fname = os.path.join(log_dir, 'json_to_csv.log')
json_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\json_data')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data\\raw_data')

logging.basicConfig(filename=gather_data_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def json_to_csv_conversion():
    data_frame = pd.DataFrame()
    cols = ['Date', 'Close', 'Volume', 'Open', 'High', 'Low']
    json_files = [file for file in glob.glob(json_dir + '\\*', recursive=False) if not os.path.isdir(file)]
    
    for file in json_files:
        filename = (os.path.basename(file).split('/')[-1])
        ticker_name = filename.split('.')[0]
        data = json.loads(file)
        logging.info("DATA %s" %data_frame)
        data_frame = pd.json_normalize(data, record_path=['tradesTable', 'rows'], meta=['date', 'close', 'volume', 'open', 'high', 'low'])
        logging.info("DATA FRAME %s" %data_frame)
        print_to_csv(data_frame, ticker_name)
        data_frame.loc[:] = None
    return

def print_to_csv(data_frame, ticker_name):
    target_dir = csv_dir
    filename = ('%s.csv' % ticker_name)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    average_fname = os.path.join(os.path.normpath(os.getcwd() + os.sep), (os.path.join(target_dir, filename)))
    logging.info(average_fname)
    data_frame.to_csv(average_fname ,encoding='utf-8')
    return

def json_to_csv():
    json_to_csv_conversion()
    return json.dumps({"success": True}), 201