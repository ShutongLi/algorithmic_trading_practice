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
        self.bid = OrderQueue('B')
        # people that are on side 'sell'
        self.ask = OrderQueue('S')

    def react_to_order(self, new_order):
        if new_order['Side'] == 'B':
            self.bid.add_task(deepcopy(new_order))
        else:
            self.ask.add_task(deepcopy(new_order))

    def match_order(self, new_order):
        #
        pass

    def modify_order(self, new_order):
        oid, quant, price = itemgetter(*['OrderID', 'Quantity', 'Price'])(new_order)
        pointer_we_maintain = self.lookup[oid]
        pointer_we_maintain['Quantity'] = quant
        pointer_we_maintain['Price'] = price
        # TODO:// UPDATE PRIORITY IN heapq while MAINTAINING QUEUE INVARIANCE, AHHHHHHHHHHHHHHHH
        # if quant from one side > the other, find next best fit
        # if can't fully fulfill, don't fulfill at all

    def return_best_order(self, side):
        book = self.bid if side == 'B' else self.ask
        # have to deepcopy, don't pass away the pointer to our internal object!
        return deepcopy(book[0])





