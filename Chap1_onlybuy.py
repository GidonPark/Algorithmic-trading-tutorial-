import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order, record, symbol
from zipline.algorithm import TradingAlgorithm
import requests

start = datetime.datetime(2010, 1 ,2)
end = datetime.datetime(2019, 12, 2)

data = web.DataReader("AAPL", "yahoo", start, end)
data = data[['Adj Close']]
data.columns = ["AAPL"]
data = data.tz_localize("UTC")


plt.plot(data.index, data['AAPL'])
plt.show()

def initialize(context): #initial asset and trading pay
    pass

#Buy one APPLE stock every day
def handle_data(context, data):
    order(symbol('AAPL'), 1)
    record(AAPL=data.current(symbol('AAPL'), 'price'))

if __name__ == "__main__":
    algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
    result = algo.run(data)
    print(result[['starting_cash', 'ending_cash', 'ending_value']].tail())

    plt.plot(result.index, result.portfolio_value)
    plt.show()