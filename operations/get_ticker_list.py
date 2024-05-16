from queue import *
import logging
import os 
import pandas as pd 
import glob
from flask import json
from ticker_class import stock_ticker

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
ticker_list_log_name = os.path.join(log_dir, 'ticker_list.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data\\monthly_averages')

logging.basicConfig(filename=ticker_list_log_name, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def get_ticker_list():
    ticker_list = []
    csv_files = [file for file in glob.glob(csv_dir + '\\*', recursive=False) if not os.path.isdir(file)]
    
    for file in csv_files:
        target_file = file.split('monthly_averages\\', 1)[1].split('.csv', 1)[0].split('_monthly_average', 1)[0]
        logging.info("Target file to append: %s" %target_file)
        ticker_company_name = match_stock_symbol(target_file)
        ticker_obj = stock_ticker(ticker_company_name, target_file)
        ticker_list.append(ticker_obj)
    return json.dumps(ticker_list, default = obj_dict)

def obj_dict(obj):
    return obj.__dict__

def match_stock_symbol(target_symbol):
    input_file_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data')
    input_file = os.path.join(input_file_dir, 'Tickers.json')
    with open(input_file) as ticker:
        tickers = json.load(ticker)
        for x in tickers['Data']:
            if (x['Symbol']) == target_symbol:
                return x['Company Name']
            else: continue