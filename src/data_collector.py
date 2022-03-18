__author__ = 'Shiyi Zheng, Yuting Zhou, Shutong Li,'
import pandas as pd
import itertools


class DataCollector:
    def __init__(self):
        self.historical_data = pd.DataFrame(columns=['Symbol', 'Description', 'OrderID', 'Quantity', 'Action',
                                                     'Exchange', 'Side', 'Price', 'News'])
        self.historical_data_by_symbol = {}
        self.counter = itertools.count()
        # self.ts = TradingStrategy()

    def populate_historical_data(self, new_order):
        idx = next(self.counter)
        self.historical_data.loc[idx] = new_order
        symbol = new_order["Symbol"]

        if symbol not in self.historical_data_by_symbol.keys():
            self.historical_data_by_symbol[symbol] = pd.DataFrame(columns=['Symbol', 'Description', 'OrderID', 'Quantity',
                                                                           'Action', 'Exchange', 'Side', 'Price', 'News'])
        self.historical_data_by_symbol[symbol] = self.historical_data_by_symbol[symbol].append(new_order, ignore_index=True)

    def __repr__(self):
        return repr(self.historical_data)

    def get_historical_data(self, symbol):
        return self.historical_data[self.historical_data.Symbol == symbol]