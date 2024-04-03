from queue import *
import logging
import os 
import pandas as pd 
import glob
import re

from flask import json, request

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
baseline_average_log_fname = os.path.join(log_dir, 'identify_average.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data\\raw_data')


logging.basicConfig(filename=baseline_average_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def percent_to_float(input_string):
    logging.info("De-percenting %s", input_string)
    input_string = input_string.strip()
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
    average_frame = pd.DataFrame(columns = ['ticker', 'percent'])
    for file in csv_files:
        filename = (os.path.basename(file).split('/')[-1])
        ticker_name = filename.split('.')[0]
        logging.info("Starting average check on %s", filename)
        data_frame = pd.read_csv(file, header=0, nrows = timeframe_days)
        data_frame = data_frame.loc[:, ~data_frame.columns.str.contains('^Unnamed')]
        average = float(check_average(data_frame, timeframe_days))
        logging.info("Average: %s", average)
        average_frame = pd.concat([pd.DataFrame([[ticker_name, average]], columns = average_frame.columns), average_frame], ignore_index = True)
        data_frame.loc[:] = None
    return average_frame

def check_average(input_data_frame, time_period):
    average = 0
    percent_column = None
    percent_column = input_data_frame[['percent']]
    percent_column_time_period_data = percent_column.head(time_period)
    percent_column_sum = percent_column_time_period_data.sum()
    average = percent_column_sum / time_period
    return average

def print_average(data_frame, timeframe_days):
    target_dir = 'historical_data\\csv_data\\time_period_averages'
    filename = ('%s_day_average.csv' % timeframe_days)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    average_fname = os.path.join(os.path.normpath(os.getcwd() + os.sep), (os.path.join(target_dir, filename)))
    logging.info("Writing results to %s" %average_fname)
    data_frame.to_csv(average_fname ,encoding='utf-8')
    return

def time_period_average():
    timeframe_days = request.get_json().get('timeframe')
    logging.info("Timeframe of %s days.", timeframe_days)
    average_frame = iterate_pull_data(timeframe_days)
    print_average(average_frame, timeframe_days)
    return json.dumps({"success": True}), 201


