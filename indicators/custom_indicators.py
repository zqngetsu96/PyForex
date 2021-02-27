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

def create_zigzag(rates, pct=0.35):
    ut = 1 + pct / 100
    dt = 1 - pct / 100
    ld = rates.index[0]
    lp = rates.Close[ld]
    tr = None

    zzd, zzp = [ld], [lp]

    for ix, ch, cl in zip(rates.index, rates.High, rates.Low):
        # No initial trend
        if tr is None:
            if ch / lp > ut:
                tr = 1
            elif cl / lp < dt:
                tr = -1
        # Trend is up
        elif tr == 1:
            # New H
            if ch > lp:
                ld, lp = ix, ch
            # Reversal
            elif cl / lp < dt:
                zzd.append(ld)
                zzp.append(lp)

                tr, ld, lp = -1, ix, cl
        # Trend is down
        else:
            # New L
            if cl < lp:
                ld, lp = ix, cl
            # Reversal
            elif ch / lp > ut:
                zzd.append(ld)
                zzp.append(lp)

                tr, ld, lp = 1, ix, ch

    # Extrapolate the current trend
    if zzd[-1] != rates.index[-1]:
        zzd.append(rates.index[-1])

        if tr is None:
            zzp.append(rates.Close[zzd[-1]])
        elif tr == 1:
            zzp.append(rates.High[zzd[-1]])
        else:
            zzp.append(rates.Low[zzd[-1]])

    x = pd.Series(zzp, index=zzd)
    x = x.reindex(pd.date_range(start=rates.index.min(),
                                                  end=rates.index.max(),
                                                  freq='H'))
    x = x[x.index.dayofweek < 5]
    rates ['ZigZag'] = x
    rates['ZigZag'] = rates['ZigZag'].interpolate()
    keys = ['ZigZag']
    return keys