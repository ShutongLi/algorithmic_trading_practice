#!/bin/python3
import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import h5py
from collections import deque
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

#
# def load_financial_data(start_date, end_date,output_file):
#     try:
#         df = pd.read_pickle(output_file)
#         print('File data found...reading GOOG data')
#     except FileNotFoundError:
#         print('File not found...downloading the GOOG data')
#         df = data.DataReader('GOOG', 'yahoo', start_date, end_date)
#         df.to_pickle(output_file)
#     return df
#
# goog_data=load_financial_data(start_date='2001-01-01',
#                     end_date = '2018-01-01',
#                     output_file='goog_data.pkl')



class ForLoopBackTester:
    def __init__(self):
        self.list_position=[]
        self.list_cash=[]
        self.list_holdings = []
        self.list_total=[]

        self.long_signal=False
        self.position=0
        self.cash=10000
        self.total=0
        self.holdings=0

        self.market_data_count=0
        self.prev_price = None
        self.statistical_model = None


        # HERE YOU SHOULD REDEFINE WHAT YOU NEED FOR YOUR ML MODEL
        # IT MEANS YOU CAN CHANGE Trade, Price, OpenClose,....
        # YOU CAN USE WHATEVER YOU WANT
        # YOU CAN ALSO LEAVE IT AS IT IS
        # YOUR CHOICE....
        self.historical_data = pd.DataFrame(columns=['Trade','Price','OpenClose','HighLow'])


        self.chosen_model = None


    def buildModel(self,price_update):
        ### IN THIS PART YOU WILL NEED TO BUILD A MODEL WITH MACHINE LEARNING
        ### IT MEANS THAT YOU MUST USE ONE OF THE MACHINE LEARNING WE STUDIED
        ### logistict regression, svm, association rules, decision trees,....

        if self.prev_price is not None:
            self.historical_data.loc[self.market_data_count] = \
                [1 if price_update['price'] > self.prev_price else -1,
                 price_update['price'],
                 price_update['open'] - price_update['close'],
                 price_update['high'] - price_update['low']
                 ]
        self.prev_price = price_update['price']


        if self.market_data_count == 1000:
            pass
            # HERE YOU WILL NEED TO FIT THE MODEL


    def onMarketDataReceived(self,price_update):
        self.buildModel(price_update)
        if self.chosen_model is not None:
            pass
            ### THIS IS THE PART WHERE YOU WILL NEED TO CHANGE THE CODE
            ### YOU WILL CERTAINLY NEED TO USE A PREDICTION HERE


        ### THIS IS THE NATIVE STRATEGY THAT YOU NEED TO BEAT
        self.market_data_count += 1
        if self.market_data_count==1 or self.market_data_count == 1300:
            return 'buy'
        if self.market_data_count == 1000 or self.market_data_count == 1200:
            return 'sell'
        return 'hold'

    def buy_sell_or_hold_something(self,price_update,action):
        if action == 'buy':
            cash_needed = 100 * price_update['price']
            if self.cash - cash_needed >=0:
                print(str(price_update['date']) +
                      " send buy order for 10 shares price=" + str(price_update['price']))
                self.position += 100
                self.cash -= cash_needed
            else:
                print('buy impossible because not enough cash')


        if action == 'sell':
            position_allowed=100
            if self.position-position_allowed>=-position_allowed:
                print(str(price_update['date'])+
                      " send sell order for 10 shares price=" + str(price_update['price']))
                self.position -= position_allowed
                self.cash -= -position_allowed * price_update['price']
            else:
                print('sell impossible because not enough position')

        self.holdings = self.position * price_update['price']
        self.total = (self.holdings + self.cash)
        # print('%s total=%d, holding=%d, cash=%d' %
        #       (str(price_update['date']),self.total, self.holdings, self.cash))

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.holdings+self.cash)


naive_backtester=ForLoopBackTester()
for i in range(len(goog_data)):
    date=goog_data.index[i]
    price=goog_data['Adj Close'][i]
    high=goog_data['High'][i]
    low = goog_data['Low'][i]
    closep=goog_data['Close'][i]
    openp = goog_data['Open'][i]
    volume = goog_data['Volume'][i]

    price_information={'date' : date,
                      'price' : float(price),
                       'high' : float(high),
                       'low': float(low),
                       'close' : float(closep),
                       'open' : float(openp),
                       'volume' : float(volume)}
    action = naive_backtester.onMarketDataReceived(price_information)
    naive_backtester.buy_sell_or_hold_something(price_information,action)



plt.legend()
plt.title=('PNL')


plt.plot(naive_backtester.list_total,\
         label="Holdings+Cash using Naive BackTester")
plt.show()
print("PNL:" + str(naive_backtester.list_total[-1]-10000))
