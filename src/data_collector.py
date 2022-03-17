import pandas as pd
import itertools


class DataCollector:
    def __init__(self):
        self.historical_data = pd.DataFrame(columns=['Symbol', 'Description', 'OrderID', 'Quantity', 'Action', 'Exchange',
       'Side', 'Price', 'News'])
        self.counter = itertools.count()

    def populate_historical_data(self, new_order):
        # print('populating historical data')
        idx = next(self.counter)
        self.historical_data.loc[idx] = new_order

    def __repr__(self):
        return repr(self.historical_data)
