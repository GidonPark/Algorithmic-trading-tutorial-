import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order_target, record, symbol
from zipline.algorithm import TradingAlgorithm

start = datetime.datetime(2010, 1 ,2)
end = datetime.datetime(2019, 12, 2)

data = web.DataReader("AAPL", "yahoo", start, end)
data = data[['Adj Close']]
data.columns = ["AAPL"]
data = data.tz_localize("UTC")


plt.plot(data.index, data['AAPL'])
plt.show()

def initialize(context): #initial asset and trading pay

    context.i = 0 #cumulative trading days
    context.sym = symbol('AAPL')
    context.hold = False #Doesn't hold shares at initial time

#MA Strategy
def handle_data(context, data):

    context.i += 1
    if context.i < 20:
        return

    buy = False
    sell = False

    ma5 = data.history(context.sym, 'price', 5, '1d').mean() #5-day simple moving average
    ma20 = data.history(context.sym, 'price', 20, '1d').mean() #20-day simple moving average

    if ma5 > ma20 and context.hold == False: #Golden-cross
        order_target(context.sym, 100)
        context.hold = True
        buy = True

    elif ma5 < ma20 and context.hold == True:          #Dead-cross
        order_target(context.sym, -100)
        context.hold = False
        sell = True

    record(AAPL=data.current(context.sym, "price"), ma5=ma5, ma20=ma20, buy=buy, sell=sell)

if __name__ == "__main__":

    algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
    result = algo.run(data)
    print(result[['starting_cash', 'ending_cash', 'ending_value']].tail())

    #Reward
    plt.title('Profit')
    plt.plot(result.index, result.portfolio_value)
    plt.show()

    #trading point
    plt.title('Moving average(^: Buy, v:Sell)')
    plt.plot(result.index, result.ma5)
    plt.plot(result.index, result.ma20)
    plt.legend(loc = 'best')
    plt.plot(result.ix[result.buy == True].index, result.ma5[result.buy == True], '^')
    plt.plot(result.ix[result.sell == True].index, result.ma5[result.sell == True], 'v')
    plt.show()
