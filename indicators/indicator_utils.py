import pandas as pd
import numpy as np


def regression(rates,price):
    def my_fn(window_series):
        # Note: you can do any kind of offset here
        window_df = rates[(rates.index >= window_series.index[0]) & (rates.index <= window_series.index[-1])]
        p = np.poly1d(np.polyfit(window_df['timestamp'].values,window_df[price].values,3))
        return p(window_df['timestamp'].iloc[-1])
    return my_fn