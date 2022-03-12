import pandas as pd
from collections import defaultdict
from operator import itemgetter


class DataCollector:
    def __init__(self):
        self.historical_data = defaultdict(list)

    def get_data(self, symbol, side):
        assert side in {'buy', 'sell'}, "side argument has to be either 'buy' or 'sell'"
        if side == 'buy':
            return self.buy_data[symbol]
        else:
            return self.sell_data[symbol]

    def populate_historical_data(self, new_order, features=['Price', 'News']):
        symbol, side = new_order['Symbol'], new_order['Side']
        print(f'populating historical data for {symbol}')
        row = itemgetter(*features)(new_order)
        if side == 'B':
            self.buy_data[symbol].append(row)
        else:
            self.sell_data[symbol].append(row)

    def react_to_new_order(self, new_order):
        '''
        wrapper function for all operations pertinent to reacting to a new order from orderbook's side
        :param new_order: the new order received from server
        :return: None for now
        '''
        print("trader's orderbook reacting ")
        self.populate_historical_data(new_order)
