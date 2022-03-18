__author__ = 'Shiyi Zheng'
# from DataCollector import DataCollector
# from TradingStrategy import TradingStrategy
from collections import defaultdict

import pandas as pd


class TradeManager:
    def __init__(self, df):
        self.position = defaultdict(int)
        self.balance = 1000000
        self.holdings = 0
        self.__validated = False
        self.pnl = 0
        self.dc = df

    def __repr__(self):
        to_return = f'position: {self.position}\nbalance: {self.balance}\n' \
                    f'holding: {self.holdings}\npnl: {self.pnl}'
        return to_return

    def on_ts_trade(self, order):
        self.__validated = False
        self.__validated = self.validate_order(order)
        if self.__validated:
            symbol = order['Symbol']
            # if there is no position for this symbol, update current position
            if symbol not in self.position.keys():
                self.position[symbol] = order['Quantity']

            if order['Side'] == 'B':
                self.position[symbol] += order['Quantity']
                self.balance -= order['Quantity'] * order['Price']

            elif order['Side'] == 'S':
                self.position[symbol] -= order['Quantity']
                self.balance += order['Quantity'] * order['Price']

        self.pnl = self.get_pnl()
        # print(f"pnl = {self.pnl}")
        return self.back_to_server(order)

    def validate_order(self, order):
        '''
        buy order:  check if there is enough balance
        sell order: check if there is enough positions

        if True: call ts_trade
        else: call back_to_server -> nothing to trade
        '''
        try:
            decision = order['Side']
            if decision == 'B':
                # print('HELLO????')
                # print(self.balance, order['Price'] * order['Quantity'])
                return self.balance >= order['Price'] * order['Quantity']
            elif decision == 'S':
                return self.position[order['Symbol']] >= order['Quantity']
            # side == None : nothing to trade, send directly to server
            else:
                return False
        except TypeError as e:
            # print(e)
            return False

    def get_pnl(self):
        self.holdings = 0
        for sym, qty in self.position.items():
            xiao_df = self.dc.historical_data_by_symbol[sym]
            try:
                latest_price = xiao_df.loc[xiao_df['Side'] == 'B']['Price'].iloc[-1]
            except IndexError:
                print('no most recent buy price')
                latest_price = 0
            self.holdings += latest_price * qty
        return self.balance + self.holdings

    def back_to_server(self,order):
        if self.__validated:
            return order
        else:
            return None

