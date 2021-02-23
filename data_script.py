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


X_buy_train, Y_cls_buy_train, Y_reg_buy_train, 
X_sell_train, Y_cls_sell_train, Y_reg_sell,
X_hold_train, Y_cls_hold_train, Y_reg_hold_train = generate_data(rates, 
                                                            r = train_test_ratio,
                                                            test = False,
                                                            save_img = True)
                                                                                       
X_buy_test, Y_cls_buy_test, Y_reg_buy_test, 
X_sell_test, Y_cls_sell_test, Y_reg_sell_test, 
X_hold_test, Y_cls_hold_test, Y_reg_hold_test = generate_data(rates, 
                                                         r = train_test_ratio, 
                                                         test = True, 
                                                         save_img = True)
                                                                                                                                                    
                                                                                                                                                    
