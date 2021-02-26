import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as tb
from talib import stream
import mplfinance as mpf

from data_utils.get_data import *
from indicators.indicators_backtest import *
from indicators.custom_indicators_backtest import *

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover



class Strat(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 500
    
    def init(self):
        # Precompute the two moving averages

        _,_,_ = self.I(reg_envelopes,self.data,price='Close',deviation = 0.008, reg_window=250, reg_mean=75, env_mean = 200, bands_mean = 200, bbdev = 2)
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        """if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()"""

path = './data/csv/EURUSD.s60.csv'
rates = load_frames(path)[-1000:]

bt = Backtest(rates, Strat, cash=10_000, commission=.002)
stats = bt.run()
print(stats)

bt.plot()