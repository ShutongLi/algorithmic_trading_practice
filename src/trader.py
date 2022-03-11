import pandas as pd
from src.orderbook import OrderBook
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import h5py
from collections import deque
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression


class Trader:
    def __init__(self):
        self.order_book = OrderBook()
        # TODO:// is this supposed to be a statistical model or a object with rule-based behavior
        self.strategy = None

    def update_orderbook(self, new_order):
        self.order_book.react_to_new_order(new_order)

    # TODO://
    def react_to_new_order(self, new_order):
        self.update_orderbook(new_order)
        # self.make_trading_decision()
        pass
