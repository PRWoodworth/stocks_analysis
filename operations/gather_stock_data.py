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

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
log_fname = os.path.join(log_dir, 'get_stock_data.log')

logging.basicConfig(filename=log_fname, encoding='utf-8', level=logging.DEBUG, filemode = "w")

data = []
symbol = []
num_threads = 40

def query_stock_data(stock_ticker_list, task_number):
    to_date = date.today()
    from_date = to_date - relativedelta(years=10)
    str_to_date = to_date.strftime('%Y-%m-%d')
    str_from_date = from_date.strftime('%Y-%m-%d')
    z = 0
    headers = {"User-Agent": "PostmanRuntime/7.36.1"}
    while True:
        s = requests.session()
        tickerName = stock_ticker_list.get()
        if tickerName is None:
            next()
        logging.info("Worker task %s beginning on ticker %s", task_number, tickerName)
        work_start = time.time()
        url = "https://api.nasdaq.com/api/quote/" + tickerName + "/historical?assetclass=stocks&fromdate=" + str_from_date + "&limit=2517&todate=" + str_to_date
        information = json.loads(s.get(url, headers=headers, timeout=10).content)
        filename = "historical_data/json_data/" + tickerName + ".json"
        json_data = json.dumps(information, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(json_data)
            outfile.close
        stock_ticker_list.task_done()
        work_done = time.time()
        work_total = work_done - work_start
        logging.info("Worker task %s completed on ticker %s after %s seconds.", task_number, tickerName, work_total)
        s.close()


def read_stock_tickers():
    input_file_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'historical_data')
    input_file = os.path.join(input_file_dir, 'Tickers.json')
    with open(input_file) as ticker:
        tickers = json.load(ticker)
        for x in tickers['Data']:
            symbol.append(x['Symbol'])
    return symbol
        

def main():
    start = time.time()
    stock_ticker_list = read_stock_tickers()
    stock_ticker_queue = Queue()
    for i in range(num_threads): 
        threading.Thread(target = query_stock_data, args = (stock_ticker_queue,i,)).start()

    for x in stock_ticker_list:
        stock_ticker_queue.put(x)

    stock_ticker_queue.join()
    end = time.time()
    duration = end - start 
    logging.info("All stock tickers queried in %s seconds.", duration)
    sys.exit()

if __name__ == '__main__':
    main()

