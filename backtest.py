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


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    deviation = 0.8 / 100
    mean = pd.Series(values).rolling(n).mean()
    return mean,mean+mean*deviation,mean-mean*deviation

class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20
    
    def init(self):
        # Precompute the two moving averages
        self.sma1,self.sma_upper,self.sma_lower = self.I(SMA, self.data.Close, self.n1)
    
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

path = './data/csv/EURUSD60.csv'
rates = load_frames(path)

bt = Backtest(rates, SmaCross, cash=10_000, commission=.002)
stats = bt.run()
print(stats)

bt.plot()