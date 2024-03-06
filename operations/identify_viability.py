# TODO: go through all historical CSV data, identify tickers with average % change of 0% to X% over a time period

import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from queue import *
import threading
import time 
import logging
import os 
import sys
import pandas as pd 
import glob

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
log_fname = os.path.join(log_dir, 'identify_viability.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data')

logging.basicConfig(filename=log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def iterate_pull_data():
    data_frame = pd.DataFrame() 
    csv_files = glob.glob(csv_dir + '\\*')
    for file in csv_files:
        logging.info("Starting baseline viability check on %s", file)
        data_frame = pd.read_csv(file)
        viability = check_viability(data_frame, 30)
        print_viability(viability, data_frame)
        data_frame.loc[:] = None

def check_viability(input_data_frame, time_period):
    viability = 0
    percent_column = input_data_frame[["Percent"]]
    percent_column_time_period_data = percent_column.head(time_period)
    percent_column_sum = percent_column_time_period_data.sum()
    viability = percent_column_sum / time_period
    return viability

# TODO: generate CSV file of identified viable tickers
def print_viability(viability, data_frame):
    # TODO: append to output file
    return

def main():
    iterate_pull_data()
    sys.exit()

if __name__ == '__main__':
    main()
