# TODO: go through all historical CSV data, identify tickers with average % change of 0% to X%

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

logging.basicConfig(filename=dir_path+'/logs/identify_viability.log', encoding='utf-8', level=logging.DEBUG, filemode = "w")

def iterate_pull_data():
    data_frame = pd.DataFrame() 
    for file in os.listdir(dir_path + "./historical_data/csv_data"):
        df = pd.read_csv(file) 
        data_frame.append(df) 
        viability = check_viability(data_frame)
        print_viability(viability, data_frame)
        data_frame.iloc[0:0]

def check_viability(input_data_frame):
    viability = 0
    # TODO: average past 30 days of stock 
    return viability

# TODO: generate CSV file of identified viable tickers
def print_viability(viability, data_frame):
    # TODO: append to output file
    return