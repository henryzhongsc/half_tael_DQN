import numpy as np
import pandas as pd

from .utils import *

def average_true_range(high, low, close, n=14, fillna=False):
    """
    Name : Average True Range (ATR)
    Reference : http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr
    """
    cs = close.shift(1)
    tr = high.combine(cs, max) - low.combine(cs, min)

    atr = np.zeros(len(close))
    atr[0] = tr[1::].mean()
    for i in range(1, len(atr)):
        atr[i] = (atr[i-1] * (n-1) + tr.iloc[i]) / float(n)

    atr = pd.Series(data=atr, index=tr.index)

    if fillna:
        atr = atr.replace([np.inf, -np.inf], np.nan).fillna(0)

    return pd.Series(atr, name='atr')

def bollinger_mavg(close, n=20, fillna=False):
    """
    Name : Bollinger Bands
    N-period simple moving average (MA).
    Reference : https://en.wikipedia.org/wiki/Bollinger_Bands
    """
    mavg = close.rolling(n, min_periods=0).mean()
    if fillna:
        mavg = mavg.replace(
            [np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(mavg, name='mavg')

def bollinger_hband_indicator(close, n=20, ndev=2, fillna=False):
    """
    Name : Bollinger High Band Indicator
    Returns 1, if close is higher than bollinger high band. Else, return 0.
    Reference : https://en.wikipedia.org/wiki/Bollinger_Bands
    """
    df = pd.DataFrame([close]).transpose()
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    hband = mavg + ndev * mstd
    df['hband'] = 0.0
    df.loc[close > hband, 'hband'] = 1.0
    hband = df['hband']
    if fillna:
        hband = hband.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(hband, name='bbihband')
