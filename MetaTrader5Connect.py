# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import MetaTrader5 as mt5
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'qt')


# %%
# Copying data to pandas data frame
n_days = 365
n_hours = 24
n_mins = 60
aq_window  = n_days * n_hours * n_mins
plot_window = 72


# %%
# Initializing MT5 connection 
mt5.initialize()


print(mt5.terminal_info())
print(mt5.version())
stockdata = pd.DataFrame()
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1,0,100)

#rates = np.flip(rates,0)
rates.shape


# %%
data_frame = pd.DataFrame(rates,columns=['time','open','high','low','close','nn','nn1','nn2']).drop(['nn','nn1','nn2'],axis=1)


# %%
data_frame['date'] = pd.Timestamp.to_pydatetime(data_frame['time'])


# %%



# %%
data_frame.tail()


# %%
data_frame.describe()


# %%
# prepare the buy request structure
symbol = "XAUUSD"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "not found, can not call order_check()")
    mt5.shutdown()
    quit()
 
# if the symbol is unavailable in MarketWatch, add it
if not symbol_info.visible:
    print(symbol, "is not visible, trying to switch on")
    if not mt5.symbol_select(symbol,True):
        print("symbol_select({}}) failed, exit",symbol)
        mt5.shutdown()
        quit()
 
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}
 
# send a trading request
result = mt5.order_send(request)
# check the execution result
print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("2. order_send failed, retcode={}".format(result.retcode))
    # request the result as a dictionary and display it element by element
    result_dict=result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field,result_dict[field]))
        # if this is a trading request structure, display it element by element as well
        if field=="request":
            traderequest_dict=result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    print("shutdown() and quit")
    mt5.shutdown()


# %%
import time
while(True):
    print(mt5.symbol_info_tick(symbol))
    time.sleep(0.5)


# %%
def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
    dataset = dataset.shuffle(shuffle_buffer).map(lambda window: (window[:-1], window[-1]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset

series=list()
window_size = 3
forecast = []
for time in range(len(series) - window_size):
    forecast.append(model.predict(series[time:time + window_size][np.newaxis]))


# %%



