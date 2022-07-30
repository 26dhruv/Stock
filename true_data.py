from datetime import datetime
from truedata_ws.websocket.TD import TD
import pandas as pd
import ta
import talib
import pandas_ta as tax
from dateutil.relativedelta import relativedelta

n = 14
username = 'FYERS1774'
password = 'eetceFoc'

# live_port to be set to None in case subscribed only for Historical data
# Default ports are live_port=8082 & Historical_port=8092

td_app = TD(username, password, live_port=None)

symbols = ['HINDALCO', 'SRF', 'PIDILITIND', 'GRASIM', 'TATAMOTORS', 'TATASTEEL', 'BAJAJFINSV', 'JINDALSTEL', 'RAMCOCEM', 'NAM-INDIA', 'CONCOR', 'GLENMARK', 'AMBUJACEM', 'MINDTREE', 'ADANIPORTS', 'JSWSTEEL', 'CUMMINSIND', 'SBIN', 'LICHSGFIN', 'APOLLOTYRE', 'GODREJCP', 'DEEPAKNTR', 'INDUSINDBK', 'IRCTC', 'GODREJPROP', 'ICICIBANK', 'PEL', 'RECLTD', 'AUROPHARMA', 'RELIANCE', 'CIPLA',
           'GRANULES', 'TATACHEM', 'MUTHOOTFIN', 'MFSL', 'BAJFINANCE', 'NAUKRI', 'TATACONSUM', 'HDFCBANK', 'UPL', 'AXISBANK', 'AUBANK', 'ULTRACEMCO', 'ADANIENT', 'TITAN', 'NAVINFLUOR', 'SRTRANSFIN', 'GUJGASLTD', 'CHOLAFIN', 'INDIGO', 'ASIANPAINT', 'BAJAJ-AUTO', 'BAJFINANCE', 'BHARTIARTL', 'CHOLAFIN', 'EICHERMOT', 'ESCORTS', 'GRASIM', 'HDFC', 'INFY', 'JUBLFOOD', 'KOTAKBANK', 'RELIANCE', 'SBIN', 'TECHM', 'VEDL', 'WIPRO', 'ZEEL']
#symbols = ['PEL']
barsizes = ['EOD', 'WEEK']
# barsize = 'EOD'

# Gets current day 1 min data - Note if market not started / holiday, you will get a No Data ! return
# hist_data_3 = td_app.get_historic_data(symbol)

# Gets current day data with the bar size of your choice - Note if market not started / holiday, you will get a No Data ! return
# hist_data_3 = td_app.get_historic_data(symbol, bar_size=barsize)
for symobl in symbols:
    for barsize in barsizes:

        hist_data_3 = td_app.get_historic_data(
            symobl,  duration='3 Y', bar_size=barsize)

# Get Data for specified bar size for any start & end date-time. Default end time = now
# hist_data_3 = td_app.get_historic_data(symbol, start_time=datetime.datetime(2020, 9, 17, 15, 28, 0),bar_size=barsize, end_time=datetime.datetime(2020, 9, 19, 23, 59, 0))

# Get last n bars data for specific bar size. Works best with & recommended for 1/5 min bars.
# hist_data_3=td_app.get_n_historical_bars(symbol, no_of_bars=30, bar_size=barsize)

        df = pd.DataFrame(hist_data_3)
        td_app.disconnect()
        df["adx"] = tax.adx(high=df.h, low=df.l, close=df.c,
                            length=14, lensig=14)['ADX_14']

        df['OBV'] = tax.obv(close=df.c, volume=df.v)
        df['TRIX'] = tax.trix(df['c'], length=18, signal=18)[
            'TRIX_18_18']*100
        df['MACD'] = tax.macd(close=df.c, talib=None)['MACD_12_26_9']
        df['MACDs_12_26_9'] = tax.macd(close=df.c, talib=None)['MACDs_12_26_9']

        df['rsi'] = tax.rsi(df['c'])
        df['roc'] = talib.ROCP(df['c'], timeperiod=9)*100
        efi = tax.efi(close=df.c, volume=df.v)

        df['CCI'] = tax.cci(
            df['h'], df['l'], df['c'], length=20)
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
        df['EMA_5'] = tax.ema(df['c'], length=5)
        df['EMA_21'] = tax.ema(df['c'], length=21)
        df['EMA_89'] = tax.ema(df['c'], length=89)
        df['EMA_200'] = tax.ema(df['c'], length=200)

        df['HMA'] = tax.hma(df['c'], length=9)
        df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(
            df['h'], df['l'], df['c'], df['v']).volume_weighted_average_price()
        df['Aroon_Up'] = tax.aroon(high=df.h, low=df.l)['AROONU_14']
        df['Aroon_Down'] = tax.aroon(high=df.h, low=df.l)['AROOND_14']
        df['PSAR'] = ta.trend.PSARIndicator(df['h'], df['l'], df['c']).psar()
        df['TEMA'] = talib.TEMA(df['c'], timeperiod=9)

        df['MFI'] = tax.mfi(
            high=df.h, low=df.l, close=df.c, volume=df.v)
        df['CMF'] = tax.cmf(
            df['h'], df['l'], df['c'], df['v'])
        df['WMA'] = ta.trend.WMAIndicator(df['c']).wma()
        df[' NATR'] = talib.NATR(
            df['h'], df['l'], df['c'])
        bbands = tax.bbands(
            df['c'], length=20)

        kc = tax.kc(df['h'], df['l'], df['c'])
        eri = tax.eri(
            df['h'], df['l'], df['c'])
        sti = tax.supertrend(df['h'], df['l'], df['c'])
        df_list = [df, sti, eri,  kc, bbands]
        f = pd.concat([d.iloc[:, :-1] for d in df_list], axis=1)

        f['R-slope'] = talib.LINEARREG_SLOPE(df['c'])
        f['mom'] = tax.mom(df['c'])

       # print(macd.columns)
        f.to_excel(f"{symobl}--{barsize}.xlsx")
        del df
