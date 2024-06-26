from flask import json, request
from queue import *
import logging
import os 
import pandas as pd 
import glob
import plotly
import plotly.express as px


dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
graphing_log_fname = os.path.join(log_dir, 'graphing.log')
csv_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data\\csv_data\\monthly_averages\\')


logging.basicConfig(filename=graphing_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

def generate_graph(req_body):
    req_data = json.loads(req_body.get_data())
    # req_body = req_body.get_json()
    logging.info("Parsed JSON: %s" %req_data)
    ticker_to_graph = req_data['ticker']['ticker_symbol']
    # TODO: properly extract ticker_symbol from given JSON
    logging.info("TARGET TICKER: %s" %ticker_to_graph)
    target_file_path = csv_dir+ticker_to_graph+'_monthly_average.csv'
    logging.info("TARGET FILE PATH: %s" %target_file_path)
    target_file = glob.glob(target_file_path, recursive=False)
    logging.info("TARGET FILE: %s" %target_file)
    # TODO: if target ticker has no associated file, return error for user?
    with open(target_file[0]) as file:
        avg_frame = pd.read_csv(file, header=0)
        
        monthly_avg_plot = px.line(avg_frame, x="Date", y="Percent")

        graphJSON = plotly.io.to_json(monthly_avg_plot, pretty=True)

        return graphJSON