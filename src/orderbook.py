"""
BIG SADGE
"""
import pandas as pd
from collections import defaultdict
from operator import itemgetter
import heapq
from copy import deepcopy
from src.custom_priority_queue import OrderQueue


class OrderBook:
    """
    Runtime overview:
     O(log n) order modification (insertion), O(1) best-order lookup
    """
    def __init__(self):
        # people that are on side 'buy'
        self.bid = defaultdict(lambda: OrderQueue('B'))
        # people that are on side 'sell'
        self.ask = defaultdict(lambda: OrderQueue('S'))

    def react_to_order(self, new_order):
        symbol, side = new_order['Symbol'], new_order['Side']
        if side == 'B':
            book = self.bid[symbol]
        else:
            book = self.ask[symbol]
        # both 'A' and 'M' are under the same operation as long as orderid is UNIQUE!
        book.add_task(new_order)

    def match_order(self, new_order):
        #
        pass

    def return_best_order(self, side, symbol):
        book = self.bid if side == 'B' else self.ask
        # have to deepcopy, don't pass away the pointer to our internal object!
        return deepcopy(book[symbol].peek_order())





