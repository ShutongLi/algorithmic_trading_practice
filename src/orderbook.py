import pandas as pd
from collections import defaultdict
from operator import itemgetter
from collections import deque


class OrderBook:
    def __init__(self):
        # people that are on side 'buy'
        self.bid = defaultdict(list)
        # people that are on side 'sell'
        self.ask = defaultdict(list)

    def add_order(self, new_order):
        symbol, side, action, oid = itemgetter(*['Symbol', 'Side', 'Action', 'OrderID'])(new_order)
        if new_order == 'buy':
            # if it is to add an order
            if action == 'A':
                self.add_new_bid(new_order)
            elif action == 'M':
                self.modify_ask(new_order)
        else:
            if action == 'A':
                self.add_new_ask(new_order)
            elif action == 'M':
                self.modify_ask(new_order)

    def modify_bid(self, new_order):
        pass

    def modify_ask(self, new_order):
        pass

    def add_new_bid(self, new_order):
        self.bid[new_order['Symbol']].append(new_order.copy())
        self.bid[new_order['Symbol']].sort(key=lambda x: x['Price'])

    def add_new_ask(self, new_order):
        self.ask[new_order['Symbol']].append(new_order.copy())
        self.ask[new_order['Symbol']].sort(key=lambda x: x['Price'])

    def match_order(self, new_order):
        pass

    def check_against_bid(self, new_order):
        pass

    def check_against_ask(self, new_order):
        pass

    def hear_from_market(self, new_order):
        symbol, side, action, oid = itemgetter(*['Symbol', 'Side', 'Action', 'OrderID'])(new_order)
        self.add_order(new_order)
        self.match_order(new_order)




