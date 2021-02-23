import pandas as pd
import numpy as np
import talib as tb
from indicators.indicator_utils import *


def reg_envelopes(rates, price = 'Close', deviation = 0.008, reg_window=1000, reg_mean=75):
    rates["new_pol"] = (rates["Close"].rolling(reg_window).apply(regression(rates,price), raw=False)).rolling(reg_mean).mean()
    rates["new_pol_upper"] = rates["new_pol"].values + rates["new_pol"].values * deviation
    rates["new_pol_lower"] = rates["new_pol"].values - rates["new_pol"].values * deviation
    env = tb.SMA(rates['Close'],200)
    env_upper = env + env * deviation
    env_lower = env - env * deviation

    upper, middle, lower = tb.BBANDS(rates['Close'], 200, 2, 2)


    ind_upper = (env_upper + upper) / 2
    ind_lower = (env_lower + lower) / 2
    ind_mid = (env + middle) / 2
    
    rates['new_pol'] = (ind_mid+ rates['new_pol'].values)/2
    rates['new_pol_upper'] = (ind_upper+ rates['new_pol_upper'].values)/2
    rates['new_pol_lower'] = (ind_lower + rates['new_pol_lower'].values)/2
    
    keys = ['new_pol','new_pol_upper','new_pol_lower']
    
    return keys