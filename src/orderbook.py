"""
BIG SADGE
"""
import pandas as pd
from collections import defaultdict
from operator import itemgetter
import heapq
from copy import deepcopy
from src.custom_priority_queue import OrderQueue
from src.data_collector import DataCollector


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
        self.dc = DataCollector()

    def react_to_market_order(self, new_order):
        """
        The function for responding to market order
        :param new_order: new order heard from server (market)
        :return:
        """
        new_order = self.clean_order(new_order)
        print(f'receiving order {new_order}')
        symbol, side = new_order['Symbol'], new_order['Side']
        if side == 'B':
            print('it is a buy, opening bid book')
            book = self.bid[symbol]
        else:
            print('it is a sell, opening ask book')
            book = self.ask[symbol]
        # check the bid/offer against our ask/bid book
        self.match_order(new_order)
        # add or update the order, done under the same operation
        # both 'A' and 'M' are under the same operation as long as orderid is UNIQUE!
        print('attempt adding order...')

        new_order = book.add_task(new_order)
        # store data into the data_collector
        print('attempt storing data in')
        self.store_data(new_order)

    def find_order(self, book, order):
        pass

    def store_data(self, new_order):
        pass

    def clean_order(self, order):
        order = deepcopy(order)
        order = {'Symbol': order['Symbol'], 'OrderID': int(order['OrderID']), 'Price': float(order['Price']),
                 'Quantity': int(order['Quantity'])}
        return order

    def match_order(self, new_order, for_market=True):
        """
        :param new_order: the deepcopy and cleaned version of the json object received from server
        :param for_market: TODO: implement processing for orders coming from strategy
        :return: the same new_order pointer with quantity modified or None
        """
        print('attempt crossing the order...')
        symbol, side, quantity, price = new_order['Symbol'], new_order['Side'], new_order['Quantity'], new_order['Price']
        is_buying = False
        # if received a buy order, cross it in sell
        if side == 'B':
            book = self.ask[symbol]
            is_buying = True
        # else cross it in buy
        else:
            book = self.bid[symbol]
        if is_buying:
            print('cross checking sell book')
            # for every order in the selling book
            for order in book:
                try:
                    book_order_quantity, book_order_price = order['Quantity'], order['Price']
                    # if there is an ask that is <= our buy offer
                    if book_order_price <= price:
                        available_amount = min(book_order_quantity, quantity)
                        order['Quantity'] -= available_amount
                        new_order['Quantity'] -= available_amount
                        if order['Quantity'] <= 0:
                            book.remove_task(order)
                        if new_order['Quantity'] <= 0:
                            return None
                    # if price is already larger, then stop iteration
                    else:
                        print(f'no more available candidate, current state of this buy order {new_order}')
                        break
                # TypeError occurs when we try to access a mask as if it is still a dict
                except TypeError:
                    print('encountering mask, moving on')
                    continue
        else:
            print('cross checking buy book')
            # for every order in the bid book
            for order in book:
                try:
                    book_order_quantity, book_order_price = order['Quantity'], order['Price']
                    # if there is a bid that is >= our sell offer
                    if book_order_price >= price:
                        available_amount = min(book_order_quantity, quantity)
                        # quantity doesn't affect ordering in orderbook, so O(1) modification!
                        order['Quantity'] -= available_amount
                        new_order['Quantity'] -= available_amount
                        if order['Quantity'] <= 0:
                            book.remove_task(order)
                        if new_order['Quantity'] <= 0:
                            return None
                    # if price is already larger, then stop iteration
                    else:
                        print(f'no more available candidate, current state of this sell order {new_order}')
                        break
                # TypeError occurs when we try to access a mask as if it is still a dict
                except TypeError:
                    print('encountering mask, moving on')
                    continue
        return new_order

    def return_best_order(self, side, symbol):
        book = self.bid if side == 'B' else self.ask
        # have to deepcopy, don't pass away the pointer to our internal object!
        return deepcopy(book[symbol].peek_order())

    def __repr__(self):
        repr_string = \
            f'Ask Book: {self.ask}\n' \
            f'Bid Book: {self.bid}'
        return repr_string





