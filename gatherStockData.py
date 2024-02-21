import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta

data = []
symbol = []


def gather_stock_data():
    to_date = date.today()
    from_date = to_date - relativedelta(years=10)
    str_to_date = to_date.strftime('%Y-%m-%d')
    str_from_date = from_date.strftime('%Y-%m-%d')
    z = 0
    headers = {"User-Agent": "PostmanRuntime/7.36.1"}
    with open("Tickers.json") as ticker:
        tickers = json.load(ticker)
        s = requests.session()
        for x in tickers['Data']:
            symbol.append(x['Symbol'])
        for tickerName in symbol:
            print(tickerName)
            z = z + 1
            print(z)
            url = "https://api.nasdaq.com/api/quote/" + tickerName + "/historical?assetclass=stocks&fromdate=" + str_from_date + "&limit=2517&todate=" + str_to_date
            print(url)
            out = s.get(url, headers=headers, timeout=5)
            output = out.content
            information = json.loads(output)
            print(information)
            if z >= 3:
                break

        s.close()


gather_stock_data()