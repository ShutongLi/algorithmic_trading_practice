"""
BIG SADGE
"""
import pandas as pd
from collections import defaultdict
from operator import itemgetter
import heapq
from copy import deepcopy



class OrderBook:
    """
    Runtime overview:
     O(1) order modification, O(1) market order lookup, O(logn) order insertion,
    """
    def __init__(self):
        # people that are on side 'buy'
        self.bid = defaultdict(list)
        # people that are on side 'sell'
        self.ask = defaultdict(list)
        # order registry, orderid - pointer towards order
        self.lookup = {}

    def add_to_book(self, new_order):
        symbol, side, action, oid = itemgetter(*['Symbol', 'Side', 'Action', 'OrderID'])(new_order)
        book = self.bid if side == 'B' else self.ask
        # this is THE ONLY POINTER THAT WE ARE KEEPING TRACK OF
        pointer_copy = deepcopy(new_order)
        # type casting on POINTER COPY!
        pointer_copy['Quantity'] = int(pointer_copy['Quantity'])
        pointer_copy['Price'] = float(pointer_copy['Price'])
        pointer_copy['News'] = float(pointer_copy['News'])
        pointer_copy['OrderID'] = int(pointer_copy['OrderID'])
        # calculate priority for heapq
        priority_multiplier = 1 - 2 * (side == 'B')
        priority = priority_multiplier * pointer_copy['Price']
        # add to object address lookup
        self.lookup[pointer_copy['OrderID']] = pointer_copy
        # add to book
        heapq.heappush(book[symbol], (priority, pointer_copy))

    def react_to_order(self, new_order):
        if new_order['Action'] == 'M':
            self.modify_ask(new_order)
        else:
            self.add_to_book(new_order)

    def match_order(self, new_order):
        pass

    def modify_order(self, new_order):
        oid, quant, price = itemgetter(*['OrderID', 'Quantity', 'Price'])(new_order)
        pointer_we_maintain = self.lookup[oid]
        pointer_we_maintain['Quantity'] = quant
        pointer_we_maintain['Price'] = price
        # TODO:// UPDATE PRIORITY IN heapq

    def hear_from_market(self, new_order):
        symbol, side, action, oid = itemgetter(*['Symbol', 'Side', 'Action', 'OrderID'])(new_order)
        self.add_order(new_order)
        self.match_order(new_order)

    def return_best_order(self, side):
        book = self.bid if side == 'B' else self.ask
        # have to deepcopy, don't pass away the pointer to our internal object!
        return deepcopy(book[0])





