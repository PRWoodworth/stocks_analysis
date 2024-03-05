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

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
log_fname = os.path.join(log_dir, 'identify_viability.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data/csv_data')

logging.basicConfig(filename=log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def iterate_pull_data():
    data_frame = pd.DataFrame() 
    csv_files = os.listdir(csv_dir)
    for file in csv_files:
        print(file)
        logging.log("Starting baseline viability check on %s.", file)
        df = pd.read_csv(file) 
        data_frame.append(df) 
        viability = check_viability(data_frame, 30)
        print_viability(viability, data_frame)
        data_frame.iloc[0:0]

def check_viability(input_data_frame, time_period):
    viability = 0
    viability = input_data_frame['Percent'].head(time_period).sum() / time_period;
    # TODO: average past 30 days of stock 
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
