from curses import window
from signal import NSIG
from matplotlib.pyplot import axis
import numpy as np
import ta
import pandas as pd
import yfinance as yf
import talib
import math
import pandas_ta as tax
df = yf.download('COALINDIA.NS', period='max',
                 start='2022-01-01', end='2022-06-06')
df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
df['roc'] = ta.momentum.ROCIndicator(df['Close'], window=14).roc()
df['Force Index'] = ta.volume.ForceIndexIndicator(
    df['Close'], df['Volume'], window=14).force_index()
df['ADX'] = ta.trend.ADXIndicator(
    df['High'], df['Low'], df['Close'], window=14).adx()
df['CCI'] = ta.trend.CCIIndicator(
    df['High'], df['Low'], df['Close'], window=14).cci()
df['KST'] = ta.trend.KSTIndicator(df['Close'], nsig=14).kst()
df['MACD'] = ta.trend.MACD(df['Close']).macd()
df['CMO'] = talib.CMO(df['Close'], timeperiod=14)
df['Williams_r'] = ta.momentum.WilliamsRIndicator(
    df['High'], df['Low'], df['Close'], lbp=14).williams_r()
df['Stoch_%K'], df['Stoch_%D'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5,
                                             slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
df['TRIX'] = ta.trend.TRIXIndicator(df['Close'], window=14) .trix()
df['BOP'] = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
df['EMA_5'] = talib.EMA(df['Close'], timeperiod=5)
df['EMA_8'] = talib.EMA(df['Close'], timeperiod=8)
df['EMA_21'] = talib.EMA(df['Close'], timeperiod=21)
df['EMA_89'] = talib.EMA(df['Close'], timeperiod=89)
df['EMA_200'] = talib.EMA(df['Close'], timeperiod=200)


def HULMA(df,  n=14):
    wma1 = ta.trend.WMAIndicator(df['Close'], window=n).wma()
    wma2 = 2*ta.trend.WMAIndicator(df['Close'], window=n//2).wma()
    sqrt_of_n = math.sqrt(n)
    hma = ta.trend.WMAIndicator(wma2-wma1, window=int(sqrt_of_n)).wma()
    return hma


df.append
df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(
    df['High'], df['Low'], df['Close'], df['Volume'], window=14).volume_weighted_average_price()
df['HULLMA'] = HULMA(df)
df['Aroon'] = ta.trend.AroonIndicator(df['Close'], window=14).aroon_indicator()
df['PSAR'] = ta.trend.PSARIndicator(df['High'], df['Low'], df['Close']).psar()
df['TEMA'] = talib.TEMA(df['Close'], timeperiod=14)
df['OBV'] = ta.volume.OnBalanceVolumeIndicator(
    df['Close'], df['Volume']).on_balance_volume()
df['MFI'] = ta.volume.MFIIndicator(
    df['High'], df['Low'], df['Close'], df['Volume'], window=14).money_flow_index()
df['ChakinMoneyFlowIndicator'] = ta.volume.ChaikinMoneyFlowIndicator(
    df['High'], df['Low'], df['Close'], df['Volume'], window=14).chaikin_money_flow()
df['WMA'] = ta.trend.WMAIndicator(df['Close'], window=14).wma()
df['normalized ATR'] = talib.NATR(
    df['High'], df['Low'], df['Close'], timeperiod=14)
df['Bollinger Band upper band value'] = ta.volatility.BollingerBands(
    df['Close'], window=14).bollinger_hband()
df['Bollinger Band lower band value'] = ta.volatility.BollingerBands(
    df['Close'], window=14).bollinger_lband()
df['ketler_high'] = ta.volatility.KeltnerChannel(
    df['High'], df['Low'], df['Close'], window=14).keltner_channel_hband()
df['ketler_high_indicator'] = ta.volatility.KeltnerChannel(
    df['High'], df['Low'], df['Close'], window=14).keltner_channel_hband_indicator()
df['ketler_low'] = ta.volatility.KeltnerChannel(
    df['High'], df['Low'], df['Close'], window=14).keltner_channel_lband()
df['ketler_low_indicator'] = ta.volatility.KeltnerChannel(
    df['High'], df['Low'], df['Close'], window=14).keltner_channel_lband_indicator()
df['ketler_mband'] = ta.volatility.KeltnerChannel(
    df['High'], df['Low'], df['Close'], window=14) .keltner_channel_mband()
df['ketler_pband'] = ta.volatility.KeltnerChannel(
    df['High'], df['Low'], df['Close'], window=14).keltner_channel_pband()
df['ketler_wband'] = ta.volatility.KeltnerChannel(
    df['High'], df['Low'], df['Close'], window=14).keltner_channel_wband()
df['R-slope'] = talib.LINEARREG_SLOPE(df['Close'], timeperiod=14)
df['eri_BULLP_14'],  df['eri_BEARP_14'] = tax.eri(
    df['High'], df['Low'], df['Close'], length=14)
df['Pivot'] = (df['High'] + df['Low'] + df['Close'])/3
df['R1'] = (2*df['Pivot']) - df['Low']
df['S1'] = (2*df['Pivot']) - df['High']
df['R2'] = (df['Pivot']) + (df['High'] - df['Low'])
df['S2'] = (df['Pivot']) - (df['High'] - df['Low'])
df['R3'] = (df['R1']) + (df['High'] - df['Low'])
df['S3'] = (df['S1']) - (df['High'] - df['Low'])
df['R4'] = (df['R3']) + (df['R2'] - df['R1'])
df['S4'] = (df['S3']) - (df['S1'] - df['S2'])
stock = ['COALINDIA.NS']
sti = tax.supertrend(df['High'], df['Low'], df['Close'],
                     length=10, multiplier=1.0)
df_list = [df, sti]

f = pd.concat([d.iloc[:, :-1] for d in df_list], axis=1)
f.to_excel("output.xlsx",
           sheet_name='{stock}')
