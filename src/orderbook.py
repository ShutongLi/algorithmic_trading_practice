__author__ = 'Shutong Li'
import pandas as pd
from collections import defaultdict
from operator import itemgetter
import heapq
from copy import deepcopy
from src.custom_priority_queue import OrderQueue
from src.data_collector import DataCollector
from src.tradingStrategy import TradingStrategy

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
        self.ts = TradingStrategy()

    def react_to_market_order(self, new_order):
        """
        The function for responding to market order
        :param new_order: new order heard from server (market)
        :return:
        """
        # print(f'!!!receiving order {new_order}')
        # store data into the data_collector
        self.store_data(new_order)

        # type cast some values
        new_order = self.clean_order(new_order)

        # identify which orderbook (b/s) for which company to open
        symbol, side = new_order['Symbol'], new_order['Side']
        if side == 'B':
            # print('it is a buy, opening bid book')
            book = self.bid[symbol]
        else:
            # print('it is a sell, opening ask book')
            book = self.ask[symbol]
        # check the bid/offer against our ask/bid book
        new_order = self.match_order(new_order)
        # add or update the order, done under the same operation
        # both 'A' and 'M' are under the same operation as long as orderid is UNIQUE!
        book.add_task(new_order)


    def store_data(self, new_order):
        self.dc.populate_historical_data(new_order)

    def clean_order(self, order):
        # this is where the deepcopy happens
        order = deepcopy(order)
        order = {'Symbol': order['Symbol'], 'OrderID': int(order['OrderID']), 'Price': float(order['Price']),
                 'Side': order['Side'], 'Quantity': int(order['Quantity'])}
        return order

    def match_order(self, new_order, for_market=True):
        """
        :param new_order: the deepcopy and cleaned version of the json object received from server
        :param for_market: TODO: implement processing for orders coming from strategy
        :return: the same new_order pointer with quantity modified or None
        """
        # print('attempt crossing the order...')
        symbol, side, quantity, price = new_order['Symbol'], new_order['Side'], \
                                        new_order['Quantity'], new_order['Price']
        is_buying = False
        # if received a buy order, cross it in sell
        if side == 'B':
            book = self.ask[symbol]
            is_buying = True
        # else cross it in buy
        else:
            book = self.bid[symbol]
            # for every order in the selling book
        for entry in book:
            order = entry[2]
            try:
                book_order_quantity, book_order_price = order['Quantity'], order['Price']
                # if price matching condition meets (i.e. there is a sell order <= the bid of our new buy order
                # or there is a buy order >= then the ask of our current sell order)
                if self.price_match(side=side, book_price=book_order_price, order_price=price):
                    print(f'found crossing candidate for our new order {new_order}. Candidate: {order} ')
                    available_amount = min(book_order_quantity, quantity)
                    order['Quantity'] -= available_amount
                    new_order['Quantity'] -= available_amount
                    if order['Quantity'] <= 0:
                        print('the order candidate in orderbook is filled')
                        book.remove_task(order)
                    if new_order['Quantity'] <= 0:
                        print('this new order is fulfilled')
                        return None
                # if no more matching can be done (because price only goes higher), we stop the loop
                else:
                    break
            # TypeError occurs when we try to access a mask as if it is still a dict
            except TypeError:
                continue
        return new_order

    def price_match(self, side, order_price, book_price):
        # the side of the new order, if 'B', we are checking sell book, vice versa
        if side == 'B':
            return book_price <= order_price
        else:
            return book_price >= order_price

    def return_best_order(self, side, symbol):
        book = self.bid if side == 'B' else self.ask
        # have to deepcopy, don't pass away the pointer to our internal object!
        return deepcopy(book[symbol].peek_order())

    def __repr__(self):
        repr_string = \
            f'Ask Book: {self.ask}\n' \
            f'Bid Book: {self.bid}'
        return repr_string





