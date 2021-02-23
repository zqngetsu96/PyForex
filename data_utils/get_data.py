import numpy as np
import pandas as pd
import mplfinance as mpf
import os
import glob
import io
import IPython.display as IPydisplay
import matplotlib.pyplot as plt 
import cv2


def get_img_from_fig(fig, dpi=50):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def return_img(window_back,dpi = 50, rcparams = {}):
    buf = io.BytesIO()
    save = dict(fname=buf,dpi=dpi)
    s = mpf.make_mpf_style(base_mpf_style='yahoo',gridcolor='black',facecolor='black',rc=rcparams,figcolor='black')
    fig,_ = mpf.plot(window_back,type='candle',volume=True,savefig=save,style=s,returnfig = True)
    img = get_img_from_fig(fig, dpi=dpi)
    return img


paths = ['../data/chart_npy',
         '../data/gasf_npy',
         '../data/series_npy'
        ]

def load_frames(path): #takes full path
    rates = pd.read_csv(path,sep =";",names=["Date","hour","Open", "High", "Low", "Close","Volume"],parse_dates=True).reset_index(drop=True)
    rates['Date'] = pd.to_datetime(rates['Date'] + ' ' + rates['hour']) 
    rates['timestamp'] = rates.Date.values.astype(np.int64) // 10 ** 9 #int(rates['ts'].iloc[0] % 3600) to check for new hours when streaming
    del rates['hour']
    close = rates.Close.values
    rates['Date'] = pd.to_datetime(rates['Date'])
    rates = rates.set_index('Date')
    return rates


def get_default_rcparams():
    return {'axes.spines.bottom':False,
            'axes.spines.left':False,
            'axes.spines.right':False,
            'axes.spines.top':False,
            }


def generate_data(rates,r = 0.7,test = True, save_img = True, 
                  tp = 0.00500, 
                  sl = 0.00250, 
                  sl_h = 0.00250, 
                  window_range_back = 72,
                  window_range_front = 30,
                  keys = [],
                  dpi = 60,
                  rcparams = {'axes.spines.bottom':False,
                'axes.spines.left':False,
                'axes.spines.right':False,
                'axes.spines.top':False,
            }):
    
    X_buy = list() #N OHLC candles window
    X_buy_chart = list()
    X_buy_gasf = list()
    Y_reg_buy = list() #Next M values

    X_sell = list()
    X_sell_chart = list()
    X_sell_gasf = list()
    Y_reg_sell = list()

    X_hold = list()
    X_hold_chart = list()
    X_hold_gasf = list()
    Y_reg_hold = list()    
    
    save_img = save_img

        
    TP = tp
    SL_hold = sl_h
    SL = sl
    

    if test == True:
        start = window_range_back + int(r * len(rates))
        end = len(rates)
        folder = 'data/chart/test'
    else:
        start = window_range_back 
        end = int(len(rates) * r)
        folder = 'data/'
   

    if save_img == True:
        for path in paths:
            files = glob.glob(path+'/*.jpg')
            for f in files:
                os.remove(f)

    i = start
    while (i<end): #hold ops
        window_back = rates[i-window_range_back:i]
        window_front = rates[i:i+window_range_front]
        if len(window_front) < window_range_front:
            i = end
            continue
        lastclose = window_back.Close.iloc[-1]
        hold_up = window_front[window_front.High > lastclose + (SL_hold + 0.00100)]
        hold_down = window_front[window_front.Low < lastclose - (SL_hold + 0.00100)]
        if  len(hold_up) == 0 and len(hold_down) == 0: #Hold (strong consolidation or possible swing back) 
            X_hold.append(np.array(window_back.values))
            Y_reg_hold.append(np.array(window_front.values))        
            i += window_range_front
            if save_img == True:  
                img = return_img(window_back, dpi = dpi, rcparams=rcparams)
                X_hold_chart.append(img)
        else:
            i+=1
               
    i = start
    while (i<end): #buy ops
        window_back = rates[i-window_range_back:i]
        window_front = rates[i:i+window_range_front]
        if len(window_front) < window_range_front:
            i = end
            continue
        lastclose = window_back.Close.iloc[-1]
        TP_hit = window_front[window_front.High >= lastclose + TP]
        SL_hit = window_front[window_front.Low <= lastclose - SL]
        hold_up = window_front[window_front.High > lastclose + (SL_hold + 0.00100)]
        hold_down = window_front[window_front.Low <= lastclose - (SL_hold + 0.00100)]
        if (len(TP_hit) == 0 and len(SL_hit) == 0) and (len(hold_up) == 0 and len(hold_down) == 0): #Hold (strong consolidation or possible swing back) 
            i += window_range_front            
            continue
        elif len(TP_hit) > 0 and len(SL_hit) == 0: #buy (no SL hit in period but TP is hit)
            X_buy.append(np.array(window_back.values))
            Y_reg_buy.append(np.array(window_front.values))
            i += window_range_front
            if save_img == True:
                img = return_img(window_back, dpi = dpi, rcparams=rcparams)
                X_buy_chart.append(img)
        elif len(TP_hit) > 0 and len(SL_hit) > 0:  #buy (both tp and sl hit but SL is hit after TP so trade won)
            TP_hit = TP_hit.iloc[0]
            SL_hit = SL_hit.iloc[0]
            if TP_hit.timestamp < SL_hit.timestamp:       
                X_buy.append(np.array(window_back.values))
                Y_reg_buy.append(np.array(window_front.values))
                i += window_range_front
                if save_img == True:
                    img = return_img(window_back, dpi = dpi, rcparams=rcparams)
                    X_buy_chart.append(img)
            else:
                i+=1
        else:
            i+=1

                    

    #look for sells and holds
    i = start
    while (i<end): #sell_ops
        window_back = rates[i-window_range_back:i]
        window_front = rates[i:i+window_range_front]
        if len(window_front) < window_range_front:
            i = end
            continue
        lastclose = window_back.Close.iloc[-1]
        SL_hit = window_front[window_front.High >= lastclose + SL]
        TP_hit = window_front[window_front.Low <= lastclose - TP]
        
        hold_up = window_front[window_front.High > lastclose + (SL_hold + 0.00100)]
        hold_down = window_front[window_front.Low <= lastclose - (SL_hold + 0.00100)]
        
        if  (len(TP_hit) == 0 and len(SL_hit) == 0) and (len(hold_up) == 0 and len(hold_down) == 0): #Hold (strong consolidation)
            i += window_range_front
            continue
        elif len(TP_hit) > 0 and len(SL_hit) == 0: #buy (no SL hit in period but TP is hit)
            X_sell.append(np.array(window_back.values))
            Y_reg_sell.append(np.array(window_front.values))
            i += window_range_front     
            if save_img == True:
                img = return_img(window_back, dpi = dpi, rcparams=rcparams)
                X_sell_chart.append(img)
        elif len(TP_hit) > 0 and len(SL_hit) > 0:  #buy (both tp and sl hit but SL is hit after TP so trade won)
            TP_hit = TP_hit.iloc[0]
            SL_hit = SL_hit.iloc[0]
            if TP_hit.timestamp < SL_hit.timestamp:       
                X_sell.append(np.array(window_back.values))
                Y_reg_sell.append(np.array(window_front.values))
                i += window_range_front
                if save_img == True:
                    img = return_img(window_back, dpi = dpi, rcparams=rcparams)
                    X_sell_chart.append(img)    
            else:
                i+=1
        else:
            i+=1


    X_buy = np.array(X_buy) #72 OHLC candles window
    X_buy_chart = np.array(X_buy_chart)
    Y_reg_buy = np.array(Y_reg_buy) #Next 72 values


    X_sell = np.array(X_sell)
    X_sell_chart = np.array(X_sell_chart)
    Y_reg_sell = np.array(Y_reg_sell)


    X_hold = np.array(X_hold)
    X_hold_chart = np.array(X_hold_chart)
    Y_reg_hold = np.array(Y_reg_hold)


    print(X_buy.shape)
    print(Y_reg_buy.shape)
    print(X_buy_chart.shape)
    
    
    print(X_sell.shape)
    print(Y_reg_sell.shape)
    print(X_sell_chart.shape)
    
    print(X_hold.shape)
    print(Y_reg_hold.shape)
    print(X_hold_chart.shape)


    
    return X_buy, X_buy_chart, Y_reg_buy, X_sell, X_sell_chart, Y_reg_sell, X_hold, X_hold_chart, Y_reg_hold