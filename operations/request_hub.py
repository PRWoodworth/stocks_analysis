from get_time_period_average import time_period_average
from get_monthly_average import monthly_average
from gather_stock_data import gather_data
from json_to_csv import json_to_csv
from get_ticker_list import get_ticker_list
from graphing import generate_graph
import logging
import os 
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import json, request
api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
request_log_fname = os.path.join(log_dir, 'request_hub.log')

logging.basicConfig(filename=request_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

@api.route('/time_period_average', methods=['GET'])
def call_time_period_average():
    response = time_period_average()
    return response

@api.route('/monthly_average', methods = ['GET'])
def call_monthly_average():
    response = monthly_average()
    return response

@api.route('/gather_stock_data', methods=['GET'])
def call_gather_stock_data():
    response = gather_data()
    return response

@api.route('/json_to_csv', methods=['GET'])
def call_json_to_csv():
    response = json_to_csv()
    return response

@api.route('/get_ticker_list', methods=['GET'])
def compile_ticker_list():
    response = get_ticker_list()
    return response

@api.route('/get_percent_change_graph', methods=['POST'])
def pass_graph_to_web():
    logging.info("Incoming graphing request body: %s" %request)
    response = generate_graph(request)
    return response



if __name__ == '__main__':
    api.run(port=5000)