import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from queue import *
import threading
import time 


data = []
symbol = []
num_threads = 20

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
        print("Worker task",task_number,"beginning on ticker", tickerName)
        work_start = time.time()
        # z = z + 1
        # print(z)
        url = "https://api.nasdaq.com/api/quote/" + tickerName + "/historical?assetclass=stocks&fromdate=" + str_from_date + "&limit=2517&todate=" + str_to_date
        information = json.loads(s.get(url, headers=headers, timeout=5).content)
        filename = "historical_data/json_data/" + tickerName + ".json"
        json_data = json.dumps(information, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(json_data)
            outfile.close
        stock_ticker_list.task_done()
        work_done = time.time()
        work_total = work_done - work_start
        print("Worker task",task_number,"completed on ticker", tickerName, "after", work_total, "seconds.")
        s.close()


def read_stock_tickers():
    with open("./historical_data/Tickers.json") as ticker:
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
    print("All stock tickers queried in",duration,"seconds.")

if __name__ == '__main__':
    main()

