from queue import *
import logging
import os 
import pandas as pd 
import glob
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
baseline_average_log_fname = os.path.join(log_dir, 'monthly_average.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data')

logging.basicConfig(filename=baseline_average_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def get_monthly_average():
    data_frame = pd.DataFrame() 
    csv_files = glob.glob(csv_dir + '\\*')
    average_frame = pd.DataFrame(columns = ['Date', 'Percent'])
    
    for file in csv_files:
        filename = (os.path.basename(file).split('/')[-1])
        ticker_name = filename.split('.')[0]
        logging.info("Getting monthly averages from %s", filename)
        data_frame = average_frame.groupby(pd.PeriodIndex(average_frame['Date'], freq="M"))['Value'].mean().reset_index()
        data_frame = data_frame.loc[:, ~data_frame.columns.str.contains('^Unnamed')]
        data_frame.loc[:] = None
    return average_frame

def print_average(data_frame, ticker_name):
    average_fname = os.path.join(os.path.normpath(os.getcwd() + os.sep), ('historical_data\\monthly_averages\\%s_monthly_average.csv' % ticker_name))
    data_frame.to_csv(average_fname ,encoding='utf-8')
    return