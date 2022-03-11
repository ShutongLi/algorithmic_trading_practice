import pandas as pd
from collections import defaultdict
from operator import itemgetter


class OrderBook:
    def __init__(self):
        # historical data for training, hopefully these two variables are not changed outside of the class
        # symbol - price_history
        self.buy_data = defaultdict(list)
        self.sell_data = defaultdict(list)
        # symbol - my holding
        self.positions = defaultdict(int)

    def get_data(self, symbol, side):
        assert side in {'buy', 'sell'}, "side argument has to be either 'buy' or 'sell'"
        if side == 'buy':
            return self.buy_data[symbol]
        else:
            return self.sell_data[symbol]

    def populate_historical_data(self, new_order, features = ['Price', 'News']):
        symbol, side = new_order['Symbol'], new_order['Side']
        row = itemgetter(*features)(new_order)
        if side == 'B':
            self.buy_data[symbol].append(row)
        else:
            self.sell_data[symbol].append(row)

    # TODO: what else aside from populating training data?
    def react_to_new_order(self, new_order):
        '''
        wrapper function
        :param new_order: the new order received from server
        :return: None for now
        '''
        self.populate_historical_data(new_order )
        # TODO: what then


