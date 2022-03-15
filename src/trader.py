import pandas as pd
from src.orderbook import OrderBook
from src.data_collector import DataCollector
import numpy as np
import matplotlib.pyplot as plt
import h5py
from collections import deque
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression


class Trader:
    def __init__(self, deposit=10000):
        self.order_book = OrderBook()
        self.data_collector = DataCollector()
        self.deposit = deposit
        self.strategy = None

    def update_orderbook(self, new_order):
        self.order_book.react_to_order(new_order)

    def update_data_collector(self, new_order):
        self.data_collector.react_to_new_order(new_order)

    # TODO://
    def react_to_new_order(self, new_order):
        '''
        wrapper for everything
        :param new_order:
        :return:
        '''
        print(f'receiving new order: {new_order}')
        self.update_orderbook(new_order)
        # self.make_trading_decision()
        pass
