
# Load the necessary packages and modules
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance
import pandas as pd

# Force Index


def CCI(df, ndays):

    df['TP'] = (data['High'] + data['Low'] + data['Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: pd.Series(x).mad())
    df['CCI'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])
    return df


def macd(df):
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return df


def get_roc(close, n):
    difference = close.diff(n)
    nprev_values = close.shift(n)
    roc = (difference / nprev_values) * 100
    return roc


def computeRSI(data, time_window):
    diff = data.diff(1).dropna()        # diff in one field(one day)

    # this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[diff > 0]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[diff < 0]

    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=tim_window-1 so we get decay alpha=1/time_window
    up_chg_avg = up_chg.ewm(com=time_window-1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(
        com=time_window-1, min_periods=time_window).mean()

    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi


def get_kst(close, sma1, sma2, sma3, sma4, roc1, roc2, roc3, roc4, signal):
    rcma1 = get_roc(close, roc1).rolling(sma1).mean()
    rcma2 = get_roc(close, roc2).rolling(sma2).mean()
    rcma3 = get_roc(close, roc3).rolling(sma3).mean()
    rcma4 = get_roc(close, roc4).rolling(sma4).mean()
    kst = (rcma1 * 1) + (rcma2 * 2) + (rcma3 * 3) + (rcma4 * 4)
    signal = kst.rolling(signal).mean()
    return kst, signal


def get_ATR(df):
    high_low = data['High'] - data['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(14).sum()/14
    return atr


def DMI(df, period):
    df['UpMove'] = df['High'] - df['High'].shift(1)
    df['DownMove'] = df['Low'].shift(1) - df['Low']
    df['Zero'] = 0

    df['PlusDM'] = np.where((df['UpMove'] > df['DownMove']) & (
        df['UpMove'] > df['Zero']), df['UpMove'], 0)
    df['MinusDM'] = np.where((df['UpMove'] < df['DownMove']) & (
        df['DownMove'] > df['Zero']), df['DownMove'], 0)
    df['plusDI'] = 100 * (df['PlusDM']/df['ATR']).ewm(span=period,
                                                      min_periods=0, adjust=True, ignore_na=False).mean()
    df['minusDI'] = 100 * (df['MinusDM']/df['ATR']).ewm(span=period,
                                                        min_periods=0, adjust=True, ignore_na=False).mean()

    df['ADX'] = 100 * (abs((df['plusDI'] - df['minusDI'])/(df['plusDI'] + df['minusDI']))
                       ).ewm(span=period, min_periods=0, adjust=True, ignore_na=False).mean()
    return df


def ForceIndex(data, ndays):
    FI = pd.Series(data['Close'].diff(ndays) *
                   data['Volume'], name='ForceIndex')
    data = data.join(FI)
    return data


# Retrieve the Apple Inc. data from Yahoo finance:
data = pdr.get_data_yahoo("AAPL", start="2010-01-01", end="2016-01-01")
data = pd.DataFrame(data)

# Compute the Force Index for AAPL
n = 1
AAPL_ForceIndex = ForceIndex(data, n)
data['ATR'] = get_ATR(data)
DMI(data, n)
data['RSI'] = computeRSI(data['Adj Close'], 14)
data['ROC'] = get_roc(data['Close'], n)
#ROC = ROC_Nifty['Rate of Change']
NIFTY_CCI = CCI(data, n), macd(data)

data.to_excel(f'stockdata_.xlsx')
