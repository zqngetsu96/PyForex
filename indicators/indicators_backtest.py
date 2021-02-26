import pandas as pd
import numpy as np
import talib as tb
from indicators.indicator_utils import *

def Envelopes(values, n, deviation):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    mean = pd.Series(values).rolling(n).mean()
    return mean,mean+mean*deviation,mean-mean*deviation


def create_HA(rates):
    df_HA = rates.copy()
    df_HA['Close']=(rates['Open']+ rates['High']+ rates['Low']+rates['Close'])/4

    for i in range(0, len(rates)):
        if i == 0:
            df_HA['Open'][i]= ( (rates['Open'][i] + rates['Close'][i] )/ 2)
        else:
            df_HA['Open'][i] = ( (rates['Open'][i-1] + rates['Close'][i-1] )/ 2)

    df_HA['High']=rates[['Open','Close','High']].max(axis=1)
    df_HA['Low']=rates[['Open','Close','Low']].min(axis=1)
    keys = ['Open','High','Low','Close']
    return df_HA,keys

def create_percentage(values):
    return pd.Series(values).pct_change() * 100
   

def create_RSI(values,period=14):
    return tb.RSI(values, timeperiod=period)
    
def create_MACD(values, n_slow = 26, n_fast = 10, signalperiod = 9):
    macd, macdsignal, macdhist = tb.MACD(values, fastperiod=n_fast, slowperiod=n_slow, signalperiod=signalperiod)
    return macd, macdsignal

def create_bollinger_bands(values, r = 20, dev = 2):
    upperband, middleband, lowerband = tb.BBANDS(values, timeperiod=r, nbdevup=dev, nbdevdn=dev)
    return upperband, middleband,lowerband
    
def create_moving_averages(values, range1 = 21, range2 = 55, range3 = 128):
    return tb.EMA(values,range1),tb.EMA(values,range2),tb.EMA(values,range3)

