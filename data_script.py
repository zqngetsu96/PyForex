import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as tb
from talib import stream
import mplfinance as mpf
from data_utils.get_data import *

acq_window = 5000
reg_window = 1000
reg_mean = 75
deviation = 1 / 100

path = './data/csv/EURUSD60.csv'

rates = load_frames(path)
rates.tail()

sample = rates[-144:-72]

train_test_ratio = 0.5


X_buy, Y_cls_buy, Y_reg_buy, X_sell, Y_cls_sell, Y_reg_sell, X_hold, Y_cls_hold, Y_reg_hold = generate_data(rates, 
                                                            r = 1,
                                                            test = False,
                                                            save_img = True,
                                                            tp = 0.00500, 
                                                            sl = 0.00250, 
                                                            sl_h = 0.00150, 
                                                            window_range_back = 30, 
                                                            window_range_front = 15)

                                                                                                                                                    
                                                                                                                                                    
