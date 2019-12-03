import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order_target, record, symbol,set_commission, commission
from zipline.algorithm import TradingAlgorithm

start = datetime.datetime(2016, 1 ,2)
end = datetime.datetime(2016, 1, 31)

data = web.DataReader("000660.KS", "yahoo", start, end)
data = data[['Adj Close']]
data.columns = ["SKHynix"]
data = data.tz_localize("UTC")

plt.plot(data.index, data['SKHynix'])
plt.show()

def initialize(context): #initial asset and trading pay
    context.sym = symbol('SKHynix')
    set_commission(commission.PerDollar(cost=0.00165))
#only buy
def handle_data(context, data):
    order_target(context.sym, 1)

if __name__ == "__main__":

    algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
    result = algo.run(data)
    print(result[['starting_cash', 'ending_cash', 'ending_value']].tail())

    #Reward
    plt.title('Profit')
    plt.plot(result.index, result.portfolio_value)
    plt.show()