from kiteconnect import KiteConnect, KiteTicker
import kiteconnect
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import ta
import talib
import pandas_ta as tax
api_s = 'nk5og7vd8g2x6gi1290b0tjto9fmj4ol'
kws = KiteConnect(api_key='eonfg4j6cfm7svx5', access_token='pi0jF2Mwh60LW05eKpUZfNdThFJb9MjB'
                  )
nse = kws.instruments('NSE')  # replace 'NSE' with 'BSE' for BSE data
nse_data = pd.DataFrame(nse)
int_tokens = {"ADANIENT": '6401'}
barsizes = ['5minute', '15minute', '60minute']
for symbol, int_token in int_tokens.items():
    for barsize in barsizes:
        f_date = dt.date.today() - relativedelta(year=2019)
        t_date = dt.date.today()
        df = pd.DataFrame()
        while True:
            # if from_date is within the 60 days limit
            if f_date >= (t_date - dt.timedelta(100)):
                df = df.append(pd.DataFrame(kws.historical_data(
                    int_token, f_date, t_date, barsize)))
                break
            else:  # if from_date has more than 60 days limit
                t_date_new = f_date + dt.timedelta(100)
                df = df.append(pd.DataFrame(kws.historical_data(
                    int_token, f_date, t_date_new, barsize)))

            # to_date = from_date.date() + dt.timedelta(60)
                f_date = t_date_new

        df["adx"] = tax.adx(high=df.high, low=df.low, close=df.close,
                            length=14, lensig=14)['ADX_14']

        df['OBV'] = tax.obv(close=df.close, volume=df.volume)
        df['TRIX'] = tax.trix(df['close'], length=18, signal=18)[
            'TRIX_18_18']*100
        df['MACD'] = tax.macd(close=df.close, talib=None)['MACD_12_26_9']
        df['MACDs_12_26_9'] = tax.macd(close=df.close, talib=None)[
            'MACDs_12_26_9']

        df['rsi'] = tax.rsi(df['close'])
        df['roc'] = talib.ROCP(df['close'], timeperiod=9)*100
        efi = tax.efi(close=df.close, volume=df.volume)

        df['CCI'] = tax.cci(
            df['high'], df['low'], df['close'], length=20)
        df['KST'] = ta.trend.KSTIndicator(df['close']).kst()
        df['KST_Sig '] = ta.trend.KSTIndicator(df['close']).kst_sig()

        df['CMO'] = tax.cmo(close=df.close, length=9, talib=False, append=True)
        df['Williams_r'] = ta.momentum.WilliamsRIndicator(
            df['high'], df['low'], df['close']).williams_r()
        df['stoch_k'] = ta.momentum.StochasticOscillator(
            df['high'], df['low'], df['close']).stoch()
        df['stoch_d'] = ta.momentum.StochasticOscillator(
            df['high'], df['low'], df['close']).stoch_signal()

        df['BOP'] = tax.bop(df['open'], df['high'], df['low'], df['close'])
        df['EMA_5'] = tax.ema(df['close'], length=5)
        df['EMA_21'] = tax.ema(df['close'], length=21)
        df['EMA_89'] = tax.ema(df['close'], length=89)
        df['EMA_200'] = tax.ema(df['close'], length=200)

        df['HMA'] = tax.hma(df['close'], length=9)
        df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(
            df['high'], df['low'], df['close'], df['volume']).volume_weighted_average_price()
        df['Aroon_Up'] = tax.aroon(high=df.high, low=df.low)['AROONU_14']
        df['Aroon_Down'] = tax.aroon(high=df.high, low=df.low)['AROOND_14']
# df['PSAR'] = ta.trend.PSARIndicator(df['high'], df['low'], df['close']).psar()
        df['TEMA'] = talib.TEMA(df['close'], timeperiod=9)

        df['MFI'] = tax.mfi(
            high=df.high, low=df.low, close=df.close, volume=df.volume)
        df['CMF'] = tax.cmf(
            df['high'], df['low'], df['close'], df['volume'])
        df['WMA'] = ta.trend.WMAIndicator(df['close']).wma()
        df[' NATR'] = talib.NATR(
            df['high'], df['low'], df['close'])
        bbands = tax.bbands(
            df['close'], length=20)

        kc = tax.kc(df['high'], df['low'], df['close'])
        eri = tax.eri(
            df['high'], df['low'], df['close'])
        sti = tax.supertrend(df['high'], df['low'], df['close'])
        df_list = [df, sti, eri,  kc, bbands]
        f = pd.concat([d.iloc[:, :-1] for d in df_list], axis=1)

        f['R-slope'] = talib.LINEARREG_SLOPE(df['close'])
        f['mom'] = tax.mom(df['close'])
        f['date'] = f['date'].dt.tz_localize(None)
# print(macd.columns)
        f.to_excel(f"{symbol}--{barsize}.xlsx")
        del df, f
