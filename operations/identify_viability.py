from queue import *
import logging
import os 
import pandas as pd 
import glob
import re

from flask import json, request

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
baseline_viability_log_fname = os.path.join(log_dir, 'identify_viability.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data')


logging.basicConfig(filename=baseline_viability_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def percent_to_float(input_string):
    logging.info("De-percenting %s", input_string)
    input_string = input_string.strip()
    # TODO: use RegEx in below to check if input is a percent
    if(not re.fullmatch("^-?\d*(\.\d+)?%", input_string)):
        input_string = "0.00%"
    try:
        output = float(input_string.strip('%'))/100
        return output
    except: 
        logging.exception("Unable to de-percent input: %s", input_string)
    

def iterate_pull_data(timeframe_days):
    data_frame = pd.DataFrame() 
    csv_files = glob.glob(csv_dir + '\\*')
    viability_frame = pd.DataFrame(columns = ['Ticker', 'Percent'])
    for file in csv_files:
        filename = (os.path.basename(file).split('/')[-1])
        ticker_name = filename.split('.')[0]
        logging.info("Starting baseline viability check on %s", filename)
        data_frame = pd.read_csv(file, converters={'Percent':percent_to_float}, header=0, nrows = timeframe_days)
        data_frame = data_frame.loc[:, ~data_frame.columns.str.contains('^Unnamed')]
        viability = float(check_viability(data_frame, timeframe_days))
        logging.info("Baseline viability: %s", viability)
        viability_frame = pd.concat([pd.DataFrame([[ticker_name, viability]], columns = viability_frame.columns), viability_frame], ignore_index = True)
        data_frame.loc[:] = None
    return viability_frame

def check_viability(input_data_frame, time_period):
    viability = 0
    percent_column = None
    percent_column = input_data_frame[['Percent']]
    percent_column_time_period_data = percent_column.head(time_period)
    percent_column_sum = percent_column_time_period_data.sum()
    viability = percent_column_sum / time_period
    return viability

def print_viability(data_frame, timeframe_days):
    viability_fname = os.path.join(os.path.normpath(os.getcwd() + os.sep), ('historical_data\\viability_days_%s.csv' % timeframe_days))
    data_frame.to_csv(viability_fname ,encoding='utf-8')
    return

def baseline_viability():
    timeframe_days = request.get_json().get('timeframe')
    logging.info("Timeframe of %s days.", timeframe_days)
    viability_frame = iterate_pull_data(timeframe_days)
    print_viability(viability_frame, timeframe_days)
    return json.dumps({"success": True}), 201


