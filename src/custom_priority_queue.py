import heapq
import itertools
from collections import Sequence
import warnings
from copy import deepcopy

OID_FIELD = 'OrderID'


class OrderQueue(Sequence):
    """
    A priority queue for orders
    implemented based on heapq
    derived from
    """

    def __init__(self, side):
        assert side in {'B', 'S'}, "side has to be either 'B' or 'S'"
        self.queue = []
        self.counter = itertools.count()
        self.__remove_placeholder__ = '<removed-order>'
        # oid - [priority, counter, order] lookup
        self.oid_entry_lookup = {}
        self.side = side
        self.__prior_multiplier__ = (1 - 2 * int(self.side == 'B'))

    @property
    def prior_multiplier(self):
        return self.__prior_multiplier__

    @property
    def remove_placeholder(self):
        '''
        :return: the string for indicating a removed placeholder
        '''
        return self.__remove_placeholder__

    def add_task(self, order:dict):
        """
        This is both for adding and updating orders
        Example:
        # assuming it is a bid book (so high to low)
        >>> new_bid = {'Symbol': 'AAL', 'Description': 'American Airlines Group Inc',
             'OrderID': '1101', 'Quantity': '455000', 'Action': 'A', 'Exchange': '1',
             'Side': 'B', 'Price': '430.05', 'News': '0'}
        >>> bid_list = OrderQueue('B')
        >>> bid_list.add_task(new_bid)
        >>> bid_list
        [{'Symbol': 'AAL', 'OrderID': 1101, 'Price': 430.05, 'Quantity': 455000}]
        >>> new_bid_with_higher_price = {'Symbol': 'AAL', 'Description': 'American Airlines Group Inc',\
             'OrderID': '1102', 'Quantity': '455000', 'Action': 'A', 'Exchange': '1',\
             'Side': 'B', 'Price': '440.05', 'News': '0'}
        >>> bid_list.add_task(new_bid_with_higher_price)
        >>> bid_list
        [{'Symbol': 'AAL', 'OrderID': 1102, 'Price': 440.05, 'Quantity': 455000}, {'Symbol': 'AAL', 'OrderID': 1101, 'Price': 430.05, 'Quantity': 455000}]
        >>> first_bid_updated_with_higher_price = {'Symbol': 'AAL', 'Description': 'American Airlines Group Inc',\
             'OrderID': '1101', 'Quantity': '455000', 'Action': 'A', 'Exchange': '1',\
             'Side': 'B', 'Price': '1000.0', 'News': '0'}
        >>> bid_list.add_task(first_bid_updated_with_higher_price)
        >>> bid_list
        [{'Symbol': 'AAL', 'OrderID': 1101, 'Price': 1000.0, 'Quantity': 455000}, '<removed-order>', {'Symbol': 'AAL', 'OrderID': 1102, 'Price': 440.05, 'Quantity': 455000}]
        >>> bid_list.peek_order()
        {'Symbol': 'AAL', 'OrderID': 1101, 'Price': 1000.0, 'Quantity': 455000}
        """
        # if new order doesn't need to be added to orderbook (b'c it is already filled)
        if order is None:
            # print('order already filled, no need for adding...')
            return
        # print('attempt adding order...')
        oid = int(order[OID_FIELD])
        if oid in self.oid_entry_lookup:
            self.remove_task(order)
        count = next(self.counter)
        order = {'Symbol': order['Symbol'], 'OrderID': int(order['OrderID']), 'Price': float(order['Price']),
                 'Quantity': int(order['Quantity'])}
        priority = self.prior_multiplier * order['Price']
        entry = [priority, count, order]
        self.oid_entry_lookup[oid] = entry
        heapq.heappush(self.queue, entry)

    def remove_task(self, order):
        """
        'Remove' and order from the queue. In reality it only masks the element.
        Raise KeyError if not found.
        """
        oid = int(order[OID_FIELD])
        entry = self.oid_entry_lookup.pop(oid)
        entry[-1] = self.remove_placeholder

    def pop_order(self):
        """Remove and return the lowest priority task. Raise KeyError if empty."""
        while self.queue:
            priority, count, order = heapq.heappop(self.queue)
            if order is not self.remove_placeholder:
                del self.oid_entry_lookup[order[OID_FIELD]]
                return order
        raise KeyError('pop from an empty priority queue')

    def peek_order(self):
        """
        :return: the NON-REMOVED item of the highest priority
        """
        for order in self.queue:
            priority, count, order = order
            if order is not self.remove_placeholder:
                # return on first non-removed order
                return order

        warnings.warn("peeking an empty queue btw, you know what you're doing?", UserWarning)
        return None

    def __getitem__(self, item):
        return self.queue[item]

    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return str([elem[2] for elem in self.queue])
        # return str(self.queue)

