from pandas_ta import Imports
from pandas_ta.utils import get_drift, get_offset, verify_series
from pandas_ta.overlap import rma
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import talib
import yfinance
import pandas as pd
from datetime import datetime
import pandas_ta as TA

# Commodity Channel Index
start = datetime(2022, 1, 1)
end = datetime(2022, 6, 6)

stock = ['COALINDIA.NS']
# Get the NIFTY data from Yahoo finance:
data = pdr.get_data_yahoo(stock, start, end)
data = pd.DataFrame(data)

# Compute the Commodity Channel Index (CCI) for NIFTY based on the 14-day moving average
n = 14


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


def cmo(close, length=None, scalar=None, talib=None, drift=None, offset=None, **kwargs):
    """Indicator: Chande Momentum Oscillator (CMO)"""
    # Validate Arguments
    length = int(length) if length and length > 0 else 14
    scalar = float(scalar) if scalar else 100
    close = verify_series(close, length)
    drift = get_drift(drift)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None:
        return

    # Calculate Result
    if Imports["talib"] and mode_tal:
        from talib import CMO
        cmo = CMO(close, length)
    else:
        mom = close.diff(drift)
        positive = mom.copy().clip(lower=0)
        negative = mom.copy().clip(upper=0).abs()

        if mode_tal:
            pos_ = rma(positive, length)
            neg_ = rma(negative, length)
        else:
            pos_ = positive.rolling(length).sum()
            neg_ = negative.rolling(length).sum()

        cmo = scalar * (pos_ - neg_) / (pos_ + neg_)

    # Offset
    if offset != 0:
        cmo = cmo.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        cmo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cmo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    cmo.name = f"CMO_{length}"
    cmo.category = "momentum"

    return cmo


data['CMO'] = cmo(pd.Series(data['Close']), n)

data['ATR'] = get_ATR(data)
DMI(data, n)
data['RSI'] = computeRSI(data['Adj Close'], 14)
data['ROC'] = get_roc(data['Close'], n)
#ROC = ROC_Nifty['Rate of Change']
NIFTY_CCI = CCI(data, n), macd(data)

data.to_excel(f'stockdata_{stock}.xlsx')
