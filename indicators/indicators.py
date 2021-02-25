import pandas as pd
import numpy as np
import talib as tb
from indicators.indicator_utils import *


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

def create_percentage(rates, price = 'Close'):
    rates["percentage"] = rates[price].pct_change()
    keys = ['percentage']
    return keys

def create_RSI(rates,period=14, price = 'Close' ):
    price = rates[price].values
    rates['RSI'] = tb.RSI(price, timeperiod=period)
    keys = ['RSI']
    return keys
    
def create_MACD(rates, n_slow = 26, n_fast = 10, price = 'Close'):
    price = rates[price].values
    macd, macdsignal, macdhist = tb.MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
    rates['MACD'] = macd
    rates['MACDSIGNAL'] = macdsignal
    keys = ['MACD','MACDSIGNAL']
    return keys

def create_bollinger_bands(rates, r = 20, dev = 2, price = 'Close'):
    price = rates[price].values
    upperband, middleband, lowerband = BBANDS(price, timeperiod=r, nbdevup=2)
    rates['bands'] = middleband
    rates['upperband'] = upperband
    rates['lowerband'] = lowerband
    keys = ['bands','upperband','lowerband']
    return keys
    
def create_moving_average(rates, range1 = 200, range2 = 50, price = 'Close'):
    price = rates[price].values
    rates['MA1'] = tb.SMA(price,range1)
    rates["MA1diff"] = price - rates["MA1"].values
    rates['MA2'] = tb.SMA(price,range2)
    rates["MA2diff"] = price - rates["MA2"].values
    rates["MA12diff"] = rates["MA1"].values - rates["MA2"].values
    
    keys = ['MA1','MA2','MA1diff','MA2diff','MA12diff']
    return keys
