from get_time_period_average import baseline_average
from gather_stock_data import gather_data
import logging
import os 
from flask import Flask
api = Flask(__name__)

log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
request_log_fname = os.path.join(log_dir, 'request_hub.log')

logging.basicConfig(filename=request_log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

@api.route('/baseline_average', methods=['PUT'])
def call_baseline_average():
    response = baseline_average()
    return response

@api.route('/gather_stock_data', methods=['GET'])
def call_gather_stock_data():
    response = gather_data()
    return response

if __name__ == '__main__':
    api.run()