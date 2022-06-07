from truedata_ws.websocket.TD import TD
import pandas as pd
import datetime
import numpy as np
import ta
import talib
import math
import pandas_ta as tax
n = 14
username = 'FYERS1774'
password = 'eetceFoc'

history_port = 8092
# live_port to be set to None in case subscribed only for Historical data
# Default ports are live_port=8082 & Historical_port=8092

td_app = TD(username, password, live_port=None)

symbol = ['TATAMOTORS', ]
barsize = ['5min', ]
# barsize = 'EOD'

# Gets current day 1 min data - Note if market not started / holiday, you will get a No Data ! return
# hist_data_3 = td_app.get_historic_data(symbol)

# Gets current day data with the bar size of your choice - Note if market not started / holiday, you will get a No Data ! return
# hist_data_3 = td_app.get_historic_data(symbol, bar_size=barsize)

# Specify Bar size and duration in No. of Days
hist_data_3 = td_app.get_historic_data(
    symbol, start_time=datetime.datetime(2022, 3, 7, 9, 1, 0), end_time=datetime.datetime(2022, 6, 7, 3, 30, 0), bar_size=barsize)

# Get Data for specified bar size for any start & end date-time. Default end time = now
# hist_data_3 = td_app.get_historic_data(symbol, start_time=datetime.datetime(2020, 9, 17, 15, 28, 0),bar_size=barsize, end_time=datetime.datetime(2020, 9, 19, 23, 59, 0))

# Get last n bars data for specific bar size. Works best with & recommended for 1/5 min bars.
# hist_data_3=td_app.get_n_historical_bars(symbol, no_of_bars=30, bar_size=barsize)

td_app.disconnect()
df = pd.DataFrame(hist_data_3)


df['rsi'] = ta.momentum.RSIIndicator(df['c'], window=n).rsi()
df['roc'] = ta.momentum.ROCIndicator(df['c'], window=n).roc()
df['Force Index'] = ta.volume.ForceIndexIndicator(
    df['c'], df['v'], window=n).force_index()
df['ADX'] = ta.trend.ADXIndicator(
    df['h'], df['l'], df['c'], window=n).adx()
df['CCI'] = ta.trend.CCIIndicator(
    df['h'], df['l'], df['c'], window=n).cci()
df['KST'] = ta.trend.KSTIndicator(df['c'], nsig=n).kst()
df['MACD'] = ta.trend.MACD(df['c']).macd()
df['CMO'] = talib.CMO(df['c'], timeperiod=n)
df['Williams_r'] = ta.momentum.WilliamsRIndicator(
    df['h'], df['l'], df['c'], lbp=n).williams_r()
df['Stoch_%K'], df['Stoch_%D'] = talib.STOCH(df['h'], df['l'], df['c'], fastk_period=5,
                                             slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
df['TRIX'] = ta.trend.TRIXIndicator(df['c'], window=n) .trix()
df['BOP'] = talib.BOP(df['o'], df['h'], df['l'], df['c'])
df['EMA_5'] = talib.EMA(df['c'], timeperiod=5)
df['EMA_8'] = talib.EMA(df['c'], timeperiod=8)
df['EMA_21'] = talib.EMA(df['c'], timeperiod=21)
df['EMA_89'] = talib.EMA(df['c'], timeperiod=89)
df['EMA_200'] = talib.EMA(df['c'], timeperiod=200)


def HULMA(df,  n=14):
    wma1 = ta.trend.WMAIndicator(df['c'], window=n).wma()
    wma2 = 2*ta.trend.WMAIndicator(df['c'], window=n//2).wma()
    sqrt_of_n = math.sqrt(n)
    hma = ta.trend.WMAIndicator(wma2-wma1, window=int(sqrt_of_n)).wma()
    return hma


df['HULLMA'] = HULMA(df)
df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(
    df['h'], df['l'], df['c'], df['v'], window=n).volume_weighted_average_price()
df['Aroon'] = ta.trend.AroonIndicator(df['c'], window=n).aroon_indicator()
df['PSAR'] = ta.trend.PSARIndicator(df['h'], df['l'], df['c']).psar()
df['TEMA'] = talib.TEMA(df['c'], timeperiod=n)
df['OBV'] = ta.volume.OnBalanceVolumeIndicator(
    df['c'], df['v']).on_balance_volume()
df['MFI'] = ta.volume.MFIIndicator(
    df['h'], df['l'], df['c'], df['v'], window=n).money_flow_index()
df['ChakinMoneyFlowIndicator'] = ta.volume.ChaikinMoneyFlowIndicator(
    df['h'], df['l'], df['c'], df['v'], window=n).chaikin_money_flow()
df['WMA'] = ta.trend.WMAIndicator(df['c'], window=n).wma()
df['normalized ATR'] = talib.NATR(
    df['h'], df['l'], df['c'], timeperiod=n)
df['Bollinger Band upper band value'] = ta.volatility.BollingerBands(
    df['c'], window=n).bollinger_hband()
df['Bollinger Band lower band value'] = ta.volatility.BollingerBands(
    df['c'], window=n).bollinger_lband()
df['ketler_high'] = ta.volatility.KeltnerChannel(
    df['h'], df['l'], df['c'], window=n).keltner_channel_hband()
df['ketler_high_indicator'] = ta.volatility.KeltnerChannel(
    df['h'], df['l'], df['c'], window=n).keltner_channel_hband_indicator()
df['ketler_low'] = ta.volatility.KeltnerChannel(
    df['h'], df['l'], df['c'], window=n).keltner_channel_lband()
df['ketler_low_indicator'] = ta.volatility.KeltnerChannel(
    df['h'], df['l'], df['c'], window=n).keltner_channel_lband_indicator()
df['ketler_mband'] = ta.volatility.KeltnerChannel(
    df['h'], df['l'], df['c'], window=n) .keltner_channel_mband()
df['ketler_pband'] = ta.volatility.KeltnerChannel(
    df['h'], df['l'], df['c'], window=n).keltner_channel_pband()
df['ketler_wband'] = ta.volatility.KeltnerChannel(
    df['h'], df['l'], df['c'], window=n).keltner_channel_wband()
df['R-slope'] = talib.LINEARREG_SLOPE(df['c'], timeperiod=n)
eri = tax.eri(
    df['h'], df['l'], df['c'], length=n)
df['Pivot'] = (df['h'] + df['l'] + df['c'])/3
df['R1'] = (2*df['Pivot']) - df['l']
df['S1'] = (2*df['Pivot']) - df['h']
df['R2'] = (df['Pivot']) + (df['h'] - df['l'])
df['S2'] = (df['Pivot']) - (df['h'] - df['l'])
df['R3'] = (df['R1']) + (df['h'] - df['l'])
df['S3'] = (df['S1']) - (df['h'] - df['l'])
df['R4'] = (df['R3']) + (df['R2'] - df['R1'])
df['S4'] = (df['S3']) - (df['S1'] - df['S2'])
sti = tax.supertrend(df['h'], df['l'], df['c'],
                     length=n, multiplier=1.0)
df_list = [df, sti, eri]
f = pd.concat([d.iloc[:, :-1] for d in df_list], axis=1)
print(f['time'])
f.to_excel("output.xlsx",
           sheet_name='{stock}')
