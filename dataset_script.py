import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as tb
from talib import stream
import mplfinance as mpf
from data_utils.get_data import *

acq_window = 500
reg_window = 250
reg_mean = 75
deviation = 1 / 100

path = './data/csv/EURUSD.s60.csv'

rates = load_frames(path)
rates = rates[-acq_window:]
rates.tail()

sample = rates[-144:-72]

train_test_ratio = 0.5


X_buy, X_buy_chart, X_buy_gasf, Y_reg_buy, X_sell, X_sell_chart, X_sell_gasf, Y_reg_sell, X_hold, X_hold_chart, X_sell_gasf, Y_reg_hold = generate_data(rates, 
                                                            r = 1,
                                                            test = False,
                                                            save_img = True,
                                                            tp = 0.00500, 
                                                            sl = 0.00250, 
                                                            sl_h = 0.00150, 
                                                            window_range_back = 72, 
                                                            window_range_front = 15)

plt.imshow(X_buy_chart[0])
plt.show()