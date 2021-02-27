import pandas as pd
import numpy as np
import talib as tb
from indicators.indicator_utils import *
import time

def reg_envelopes(rates, price='Close', deviation = 0.008, reg_window=250, reg_mean=75, env_mean = 200, bands_mean = 200, bbdev = 2):
    rates = rates.df
    new_pol = (rates[price].rolling(reg_window).apply(regression(rates,price), raw=False)).rolling(reg_mean).mean().values
    pol_upper = new_pol + new_pol * deviation
    pol_lower = new_pol - new_pol * deviation

    env = tb.SMA(rates.Close.values,env_mean)
    env_upper = env + env * deviation
    env_lower = env - env * deviation

    upper, middle, lower = tb.BBANDS(rates.Close.values, bands_mean, bbdev,bbdev)


    ind_upper = (env_upper + upper) / 2
    ind_lower = (env_lower + lower) / 2
    ind_mid = (env + middle) / 2
    
    new_pol = (new_pol + ind_mid)/2
    pol_lower = (pol_lower + ind_lower)/2
    pol_upper = (pol_upper + ind_upper)/2

    
    return new_pol,pol_lower,pol_upper

