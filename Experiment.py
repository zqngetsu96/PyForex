import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as tb
from talib import stream
import mplfinance as mpf
from data_utils.get_data import *
from trendln import *
from indicators.indicators import *
from indicators.custom_indicators import *
from indicators.harmonics import *
from pyts.image import GramianAngularField
acq_window = 300
reg_window = 100
reg_mean = 75
deviation = 0.75 / 100

#Price to apply indicators on
price_col = 'Close'

path = './data/csv/EURUSD.s60.csv'


rates = load_frames(path)

rates = rates[-acq_window:]
rates.tail()

#print(rates.tail())

X_buy, X_buy_chart, X_buy_gasf, Y_reg_buy, X_sell, X_sell_chart, X_sell_gasf, Y_reg_sell, X_hold, X_hold_chart, X_sell_gasf, Y_reg_hold = generate_data(rates, 
                                r = 1,
                                test = False,
                                save_img = True,
                                save_gasf = True,
                                gasf_imsize= 24,
                                tp = 0.00500, 
                                sl = 0.00250, 
                                sl_h = 0.00150, 
                                window_range_back = 36, 
                                window_range_front = 15)

print(X_buy.shape)



df_HA,keys = create_HA(rates)
keys_1 = reg_envelopes(df_HA, price_col ,deviation,reg_window,reg_mean)
keys_2 = create_MACD(df_HA)
keys_3 = create_moving_average(df_HA,range1 = 55,range2 = 21)
addp = mpf.make_addplot(df_HA[keys_1])
addp2 = mpf.make_addplot(df_HA[keys_2],panel=2)
addp3 = mpf.make_addplot(df_HA[['MA1','MA2']])
mpf.plot(rates, type='candle', volume = True,addplot = [addp,addp2,addp3], style = 'yahoo',show_nontrading = False,block=False)


minimaIdxs, maximaIdxs = get_extrema(
	rates.Close,
	extmethod=METHOD_NUMDIFF,
	accuracy=2)
# parameters and results are as per defined for calc_support_resistance
Extremum_indexes = sorted(minimaIdxs + maximaIdxs)

keys = create_zigzag(rates,pct = 0.3)

addp3 = mpf.make_addplot(rates[keys])
mpf.plot(rates, type='candle', volume = True,addplot = [addp3], style = 'yahoo',show_nontrading = False,block=False)


"""
price = rates.Close
err_allowed = 0.1/100
# Find peaks
for i in range(100, len(price)):
    current_idx, current_pat, start, end = peak_detect(price.values[:i])
    plt.plot(np.arange(start, i), price.values[start:i])
    plt.scatter(current_idx, current_pat, c='r')
    plt.show()
"""

gasf = GramianAngularField(image_size=16, method='summation')
X_gasf = gasf.fit_transform(X_buy[0].transpose([1,0]))
print(X_gasf[3].shape)
plt.imshow(X_gasf[3,:])
plt.show()


while(True):
    msg = input('Close? [N],y\n')
    if msg == 'y':
        break
