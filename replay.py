import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as tb
from talib import stream
import mplfinance as mpf
import matplotlib.animation as animation
from data_utils.get_data import *
from trendln import *
from indicators.indicators import *
from indicators.custom_indicators import *

calc_window = 150
plot_window = 48

acq_window = 500
reg_window = 250
reg_mean = 75
deviation = 0.8/ 100
rn = 200
path = './data/csv/EURUSD.s60.csv'

rates = load_frames(path)
rates = rates[-acq_window:]
rates.tail()

sample = rates[-144:-72]



fig = mpf.figure(style='charles',figsize=(7,8))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(3,1,3)


def animate(ival):
    if ival+rn < calc_window:
        ival = calc_window - rn
    if (ival+rn) > len(rates):
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    data = rates.iloc[ival:ival+rn]
    ax1.clear()
    ax2.clear()
    mpf.plot(data,ax=ax1,volume=ax2,type='candle')
    mpf.show()

    
ani = animation.FuncAnimation(fig, animate, interval=100)
mpf.show()
