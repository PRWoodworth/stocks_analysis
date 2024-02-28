import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import multiprocessing


data = []
symbol = []

# TODO: fix data chunking 
def chunks(data, parts):
    divided = list()
    n = len(data) // parts
    for i in range(parts):
        divided[i] = data[i*n:n*(i+1)]
    if len(data) % 2 != 0:
        divided[-1] += [data[-1]]
    return divided

def do_job(job_id, data_slice):
    to_date = date.today()
    from_date = to_date - relativedelta(years=10)
    str_to_date = to_date.strftime('%Y-%m-%d')
    str_from_date = from_date.strftime('%Y-%m-%d')
    z = 0
    headers = {"User-Agent": "PostmanRuntime/7.36.1"}
    s = requests.session()
    for tickerName in data_slice:
        print(job_id + " " + tickerName)
        z = z + 1
        print(z)
        url = "https://api.nasdaq.com/api/quote/" + tickerName + "/historical?assetclass=stocks&fromdate=" + str_from_date + "&limit=2517&todate=" + str_to_date
        out = s.get(url, headers=headers, timeout=5)
        output = out.content
        information = json.loads(output)
        filename = "historical_data/json_data/" + tickerName + ".json"
        json_data = json.dumps(information, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(json_data)
            outfile.close
    s.close()

def dispatch_jobs(data, job_number):
    total = len(data)
    chunk_size = total / job_number
    slice = chunks(data, chunk_size)
    jobs = []
    for i, s in enumerate(slice):
        j = multiprocessing.Process(target=do_job, args=(i, s))
        jobs.append(j)
    for j in jobs:
        j.start()


def gather_stock_data():
    with open("./historical_data/Tickers.json") as ticker:
        tickers = json.load(ticker)
        for x in tickers['Data']:
            symbol.append(x['Symbol'])
    return symbol
        

def main():
    stock_ticker_list = gather_stock_data()
    dispatch_jobs(stock_ticker_list, 4)

if __name__ == '__main__':
    main()

