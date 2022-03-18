__author__ = 'Yuting Zhou'
import pandas as pd
import numpy as np
from src.data_collector import DataCollector


class TradingStrategy:
    """
    refactoring note:
    for constructor instead do
    def __init__(self, dc):
        self.dc = dc
        # no new instantiation of ob and dc
    """
    def __init__(self, dc, ob):
        self.strategy = {}
        self.trading = []
        self.ob = ob
        self.dc = dc

    def add_strategy(self, symbol):
        print(f'pattern detected for {symbol} detected')
        self.trading.append(symbol)
        company_df = pd.DataFrame.from_dict(self.dc.historical_data_by_symbol[symbol])

        new_prices = list(company_df['Price'].diff())[2:]
        news = list(company_df['News'].diff())[1:-1]
        r = np.corrcoef(news, new_prices)
        # print(news, new_prices)
        if r[0, 1] > 0.5:
            self.strategy[symbol] = ['B', 'H', 'S']
        elif r[0, 1] < -0.5:
            self.strategy[symbol] = ['S', 'H', 'B']
        else:
            self.strategy[symbol] = ['H', 'H', 'H']

    def make_decision(self, symbol):
        if len(self.dc.historical_data_by_symbol[symbol]) == 20:
            self.add_strategy(symbol)

        if symbol not in self.trading:
            return None

        company_df = pd.DataFrame.from_dict(self.dc.historical_data_by_symbol[symbol])
        news_change = int(company_df['News'][-1:]) - int(company_df['News'][-2:-1])

        if news_change > 0:
            side = self.strategy[symbol][0]
        elif news_change == 0:
            side = self.strategy[symbol][1]
        else:
            side = self.strategy[symbol][2]

        price = int(company_df['Price'][-1:])
        best_order = self.ob.return_best_order('B' if side == 'S' else 'S', symbol)
        if best_order != None:
            possible_best_order = best_order
        else:
            return {'Symbol': symbol, 'Price': price, 'Side': side, 'Quantity': 1000}

        if side == 'B':
            if possible_best_order['Quantity'] >= 1000 and possible_best_order['Price'] < price:
                price = possible_best_order['Price']
        elif side == 'S':
            if possible_best_order['Quantity'] >= 1000 and possible_best_order['Price'] > price:
                price = possible_best_order['Price']
        else:
            return None

        return {'Symbol': symbol, 'Price': price, 'Side': side, 'Quantity': 1000}

