import numpy as np
import pandas as pd
import mplfinance as mpf
import os
import glob



paths = ['./data/chart/test/buy',
    './data/chart/test/hold',
    './data/chart/test/sell',
    './data/chart/train/buy',
    './data/chart/train/hold',
    './data/chart/train/sell'
    './data/gasf/train/buy',
    './data/gasf/train/hold',
    './data/gasf/train/sell',
    './data/gasf/test/buy',
    './data/gasf/test/hold',
    './data/gasf/test/sell']

def load_frames(path): #takes full path
    rates = pd.read_csv(path,sep =";",names=["Date","hour","Open", "High", "Low", "Close","Volume"],parse_dates=True).reset_index(drop=True)
    rates['Date'] =pd.to_datetime(rates['Date'] + ' ' + rates['hour']) 
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
                  rcparams = {'axes.spines.bottom':False,
            'axes.spines.left':False,
            'axes.spines.right':False,
            'axes.spines.top':False,
            }):
    
    X_buy = list() #72 OHLC candles window
    Y_cls_buy = list() #Buy or sell depending on the next 72 candles
    Y_reg_buy = list() #Next 72 values

    X_sell = list() #72 OHLC candles window
    Y_cls_sell = list() #Buy or sell depending on the next 72 candles
    Y_reg_sell = list() #N

    X_hold = list()
    Y_cls_hold = list()
    Y_reg_hold = list()    
    
    save_img = save_img
        
    TP = tp
    SL_hold = sl_h
    SL = sl
    
    count_buy = 0
    count_sell = 0
    count_hold = 0

    fname_buy = 'window_buy_'
    fname_sell = 'window_sell_'
    fname_hold = 'window_hold_'   
    
    if test == True:
        start = window_range_back + int(r * len(rates))
        end = len(rates)
        folder = 'data/chart/test'
    else:
        start = window_range_back 
        end = int(len(rates) * r)
        folder = 'data/chart/train'
   

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
            Y_cls_hold.append(0)
            Y_reg_hold.append(np.array(window_front.values))        
            i += window_range_front
            if save_img == True:
                count_hold += 1
                save = dict(fname='./{}/hold/{}{}.jpg'.format(folder,fname_hold,count_hold),dpi=50)
                s = mpf.make_mpf_style(base_mpf_style='yahoo',gridcolor='black',facecolor='black',rc=rcparams,figcolor='black')
                mpf.plot(window_back,type='candle',volume=True,savefig=save,style=s)
    
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
            Y_cls_buy.append(1)
            Y_reg_buy.append(np.array(window_front.values))
            i += window_range_front
            if save_img == True:
                count_buy += 1
                save = dict(fname='./{}/buy/{}{}.jpg'.format(folder,fname_buy,count_buy),dpi=50)
                s = mpf.make_mpf_style(base_mpf_style='yahoo',gridcolor='black',facecolor='black',rc=rcparams,figcolor='black')
                mpf.plot(window_back,type='candle',volume=True,savefig=save,style=s)
        elif len(TP_hit) > 0 and len(SL_hit) > 0:  #buy (both tp and sl hit but SL is hit after TP so trade won)
            TP_hit = TP_hit.iloc[0]
            SL_hit = SL_hit.iloc[0]
            if TP_hit.timestamp < SL_hit.timestamp:       
                X_buy.append(np.array(window_back.values))
                Y_cls_buy.append(1)
                Y_reg_buy.append(np.array(window_front.values))
                i += window_range_front
                if save_img == True:
                    count_buy += 1
                    save = dict(fname='./{}/buy/{}{}.jpg'.format(folder,fname_buy,count_buy),dpi=50)
                    s = mpf.make_mpf_style(base_mpf_style='yahoo',gridcolor='black',facecolor='black',rc=rcparams,figcolor='black')
                    mpf.plot(window_back,type='candle',volume=True,savefig=save,style=s)
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
            Y_cls_sell.append(-1)
            Y_reg_sell.append(np.array(window_front.values))
            i += window_range_front     
            if save_img == True:
                count_sell+= 1
                save = dict(fname='./{}/sell/{}{}.jpg'.format(folder,fname_sell,count_sell),dpi=50)
                s = mpf.make_mpf_style(base_mpf_style='yahoo',gridcolor='black',facecolor='black',rc=rcparams,figcolor='black')
                mpf.plot(window_back,type='candle',volume=True,savefig=save,style=s)
        elif len(TP_hit) > 0 and len(SL_hit) > 0:  #buy (both tp and sl hit but SL is hit after TP so trade won)
            TP_hit = TP_hit.iloc[0]
            SL_hit = SL_hit.iloc[0]
            if TP_hit.timestamp < SL_hit.timestamp:       
                X_sell.append(np.array(window_back.values))
                Y_cls_sell.append(-1)
                Y_reg_sell.append(np.array(window_front.values))
                i += window_range_front
                if save_img == True:
                    count_sell+= 1
                    save = dict(fname='./{}/sell/{}{}.jpg'.format(folder,fname_sell,count_sell),dpi=50)
                    s = mpf.make_mpf_style(base_mpf_style='yahoo',gridcolor='black',facecolor='black',rc=rcparams,figcolor='black')
                    mpf.plot(window_back,type='candle',volume=True,savefig=save,style=s)      
            else:
                i+=1
        else:
            i+=1


    X_buy = np.array(X_buy) #72 OHLC candles window
    Y_cls_buy = np.array(Y_cls_buy) #Buy or sell depending on the next 72 candles
    Y_reg_buy = np.array(Y_reg_buy) #Next 72 values


    X_sell = np.array(X_sell)
    Y_cls_sell = np.array(Y_cls_sell)
    Y_reg_sell = np.array(Y_reg_sell)


    X_hold = np.array(X_hold)
    Y_cls_hold = np.array(Y_cls_hold)
    Y_reg_hold = np.array(Y_reg_hold)


    print(X_buy.shape)
    print(Y_reg_buy.shape)
    print(Y_cls_buy.shape)
    
    
    print(X_sell.shape)
    print(Y_reg_sell.shape)
    print(Y_cls_sell.shape)
    
    print(X_hold.shape)
    print(Y_reg_hold.shape)
    print(Y_cls_hold.shape)


    
    return X_buy, Y_cls_buy, Y_reg_buy, X_sell, Y_cls_sell, Y_reg_sell, X_hold, Y_cls_hold, Y_reg_hold