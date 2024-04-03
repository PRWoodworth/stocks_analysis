from dateutil.relativedelta import relativedelta
from queue import *
import pandas as pd 
import logging
import glob
import os 
from flask import json


dir_path = os.path.dirname(os.path.realpath(__file__))
json_to_csv_log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
json_to_csv_log_fname = os.path.join(json_to_csv_log_dir, 'json_to_csv.log')
json_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\json_data')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data\\raw_data')

logging.basicConfig(filename=json_to_csv_log_dir, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def json_to_csv_conversion():
    data_frame = pd.DataFrame()
    cols = ['Date', 'Close', 'Volume', 'Open', 'High', 'Low']
    json_files = [file for file in glob.glob(json_dir + '\\*', recursive=False) if not os.path.isdir(file)]
    
    for file in json_files:
        with open(file) as jsonfile:
            data = json.load(jsonfile)
            jsonfile.close()
        filename = (os.path.basename(file).split('/')[-1])
        ticker_name = filename.split('.')[0]
        data_frame = pd.json_normalize(data, record_path=['data', ['tradesTable', 'rows']])
        
        data_frame['close'] = data_frame['close'].replace({r'\$': '', ',': ''}, regex=True)
        data_frame['open'] = data_frame['open'].replace({r'\$': '', ',': ''}, regex=True)
        data_frame['high'] = data_frame['high'].replace({r'\$': '', ',': ''}, regex=True)
        data_frame['low'] = data_frame['low'].replace({r'\$': '', ',': ''}, regex=True)
        data_frame['volume'] = data_frame['volume'].replace({r'\$': '', ',': ''}, regex=True)

        data_frame = data_frame.apply(pd.to_numeric, errors='ignore')
        
        data_frame.insert(6, 'percent', (data_frame['close']/data_frame['open']-1))
        data_frame['percent'] = data_frame['percent'].apply(lambda x: round(x, 4))
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