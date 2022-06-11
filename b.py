from curses import window
import math
from signal import NSIG
from tkinter import X
from numpy import append, sign
from truedata_ws.websocket.TD import TD
import pandas as pd
import ta
import talib
import pandas_ta as tax


n = 14
username = 'FYERS1774'
password = 'eetceFoc'

history_port = 8092
# live_port to be set to None in case subscribed only for Historical data
# Default ports are live_port=8082 & Historical_port=8092

td_app = TD(username, password, live_port=None)

symbols = ['INDUSINDBK', 'TATAMOTORS']
barsizes = ['5min', '15min', 'EOD']
# barsize = 'EOD'

# Gets current day 1 min data - Note if market not started / holiday, you will get a No Data ! return
# hist_data_3 = td_app.get_historic_data(symbol)

# Gets current day data with the bar size of your choice - Note if market not started / holiday, you will get a No Data ! return
# hist_data_3 = td_app.get_historic_data(symbol, bar_size=barsize)
for symobl in symbols:
    for barsize in barsizes:

        hist_data_3 = td_app.get_historic_data(
            symobl, bar_size=barsize, duration='3    M')

# Get Data for specified bar size for any start & end date-time. Default end time = now
# hist_data_3 = td_app.get_historic_data(symbol, start_time=datetime.datetime(2020, 9, 17, 15, 28, 0),bar_size=barsize, end_time=datetime.datetime(2020, 9, 19, 23, 59, 0))

# Get last n bars data for specific bar size. Works best with & recommended for 1/5 min bars.
# hist_data_3=td_app.get_n_historical_bars(symbol, no_of_bars=30, bar_size=barsize)

        df = pd.DataFrame(hist_data_3)
        td_app.disconnect()
        df["adx"] = tax.adx(high=df.h, low=df.l, close=df.c,
                            length=14, lensig=14, mamode='rma', talib=None)['ADX_14']

        df['OBV'] = tax.obv(close=df.c, volume=df.v)
        df['TRIX'] = talib.TRIX(df['c'], timeperiod=18)*100
        df['MACD'] = tax.macd(close=df.c, talib=None)['MACD_12_26_9']
        df['MACDs_12_26_9'] = tax.macd(close=df.c, talib=None)['MACDs_12_26_9']

        df['rsi'] = tax.rsi(df['c'])
        df['roc'] = talib.ROCP(df['c'], timeperiod=9)
        df['Force Index'] = ta.volume.ForceIndexIndicator(
            df['c'], df['v']).force_index()

        df['CCI'] = ta.trend.CCIIndicator(
            df['h'], df['l'], df['c'], ).cci()
        df['KST'] = ta.trend.KSTIndicator(df['c']).kst()
        df['KST_Sig '] = ta.trend.KSTIndicator(df['c']).kst_sig()

        df['CMO'] = tax.cmo(close=df.c, length=9, talib=False, append=True)
        df['Williams_r'] = ta.momentum.WilliamsRIndicator(
            df['h'], df['l'], df['c']).williams_r()
        df['stoch_k'] = ta.momentum.StochasticOscillator(
            df['h'], df['l'], df['c']).stoch()
        df['stoch_d'] = ta.momentum.StochasticOscillator(
            df['h'], df['l'], df['c']).stoch_signal()

        df['BOP'] = tax.bop(df['o'], df['h'], df['l'], df['c'])
        df['EMA_10'] = tax.ema(df['c'], length=10)
        df['EMA_11'] = tax.ema(df['c'], length=11)
        df['EMA_20'] = tax.ema(df['c'], length=20)
        df['EMA_30'] = tax.ema(df['c'], length=30)

        df['EMA_50'] = tax.ema(df['c'], length=50)
        df['EMA_200'] = tax.ema(df['c'], length=200)

        df['HMA'] = tax.hma(df['c'], length=9)
        df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(
            df['h'], df['l'], df['c'], df['v']).volume_weighted_average_price()
        df['Aroon_down'] = ta.trend.AroonIndicator(
            df['c'], window=14).aroon_down()
        df['aroon_up'] = ta.trend.AroonIndicator(
            df['c'], window=14).aroon_up()
        df['PSAR'] = ta.trend.PSARIndicator(df['h'], df['l'], df['c']).psar()
        df['TEMA'] = talib.TEMA(df['c'])

        df['MFI'] = ta.volume.MFIIndicator(
            df['h'], df['l'], df['c'], df['v']).money_flow_index()
        df['ChakinMoneyFlowIndicator'] = ta.volume.ChaikinMoneyFlowIndicator(
            df['h'], df['l'], df['c'], df['v']).chaikin_money_flow()
        df['WMA'] = ta.trend.WMAIndicator(df['c']).wma()
        df['normalized ATR'] = talib.NATR(
            df['h'], df['l'], df['c'])
        df['Bollinger Band upper band value'] = ta.volatility.BollingerBands(
            df['c']).bollinger_hband()
        df['Bollinger Band lower band value'] = ta.volatility.BollingerBands(
            df['c']).bollinger_lband()
        kc = tax.kc(df['h'], df['l'], df['c'])
        eri = tax.eri(
            df['h'], df['l'], df['c'])
        sti = tax.supertrend(df['h'], df['l'], df['c'])
        df_list = [df, sti, eri,  kc]
        f = pd.concat([d.iloc[:, :-1] for d in df_list], axis=1)

        def hpi(df):
            prev_close = df['c'].iloc[-2:-1]

            prev_open = df['o'].iloc[-2:-1]
            prev_high = df['h'].iloc[-2:-1]
            prev_low = df['l'].iloc[-2:-1]
            medain = (df['h']+df['l'])/2

        def PPSR(df):
            df['PP'] = pd.Series((df['h'] + df['l'] + df['c']) / 3)
            df['R1'] = pd.Series(2 * df['PP'] - df['l'])
            df['S1'] = pd.Series(2 * df['PP'] - df['h'])
            df['R2'] = pd.Series(df['PP'] + df['h'] - df['l'])
            df['S2'] = pd.Series(df['PP'] - df['h'] + df['l'])
            df['R3'] = pd.Series(df['h'] + 2 * (df['PP'] - df['l']))
            df['S3'] = pd.Series(df['l'] - 2 * (df['h'] - df['PP']))

            return df
        PPSR(f)
        f['R-slope'] = talib.LINEARREG_SLOPE(df['c'])
        f['mom'] = tax.mom(df['c'])

       # print(macd.columns)
        f.to_excel(f"{symobl}--{barsize}.xlsx")
        del df
