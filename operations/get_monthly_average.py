from queue import *
import logging
import os 
import pandas as pd 
import glob
from flask import json

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
baseline_average_log_fname = os.path.join(log_dir, 'monthly_average.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data\\raw_data')

logging.basicConfig(filename=baseline_average_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def get_monthly_average():
    data_frame = pd.DataFrame() 
    csv_files = [file for file in glob.glob(csv_dir + '\\*', recursive=False) if not os.path.isdir(file)]
    average_frame = pd.DataFrame(columns = ['date', 'percent'])
    
    for file in csv_files:
        
        filename = (os.path.basename(file).split('/')[-1])
        ticker_name = filename.split('.')[0]
        logging.info("Getting monthly averages from %s", filename)
        average_frame = pd.read_csv(file, header=0)
        average_frame = average_frame.loc[:, ~average_frame.columns.str.contains('^Unnamed')]
        data_frame = average_frame.groupby(pd.PeriodIndex(average_frame['date'], freq="M"))['percent'].mean().reset_index()
        print_average(data_frame, ticker_name)
        data_frame.loc[:] = None
    return data_frame

def print_average(data_frame, ticker_name):
    target_dir = 'historical_data\\csv_data\\monthly_averages'
    filename = ('%s_monthly_average.csv' % ticker_name)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    average_fname = os.path.join(os.path.normpath(os.getcwd() + os.sep), (os.path.join(target_dir, filename)))
    logging.info(average_fname)
    data_frame.to_csv(average_fname ,encoding='utf-8')
    return

def monthly_average():
    get_monthly_average()
    return json.dumps({"success": True}), 201