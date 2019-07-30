import numpy as np
import pandas as pd

from .utils import *

def acc_dist_index(high, low, close, volume, fillna=False):
    """
    Name: Accumulation/distribution index
    Reference : https://en.wikipedia.org/wiki/Accumulation/distribution_index
    """
    clv = ((close - low) - (high - close)) / (high - low)
    clv = clv.fillna(0.0)  # float division by zero
    ad = clv * volume
    ad = ad + ad.shift(1, fill_value=ad.mean())
    if fillna:
        ad = ad.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(ad, name='adi')

def on_balance_volume(close, volume, fillna=False):
    """
    Name : on balance volume
    Reference : https://en.wikipedia.org/wiki/On-balance_volume
    """
    df = pd.DataFrame([close, volume]).transpose()
    df['OBV'] = np.nan
    c1 = close < close.shift(1)
    c2 = close > close.shift(1)
    if c1.any():
        df.loc[c1, 'OBV'] = - volume
    if c2.any():
        df.loc[c2, 'OBV'] = volume
    obv = df['OBV'].cumsum()
    if fillna:
        obv = obv.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(obv, name='obv')

def chaikin_money_flow(high, low, close, volume, n=20, fillna=False):
    """
    Name : Chaikin Money Flow 
    Reference : http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf
    """
    mfv = ((close - low) - (high - close)) / (high - low)
    mfv = mfv.fillna(0.0)  # float division by zero
    mfv *= volume
    cmf = (mfv.rolling(n, min_periods=0).sum()
           / volume.rolling(n, min_periods=0).sum())
    if fillna:
        cmf = cmf.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(cmf, name='cmf')

def volume_price_trend(close, volume, fillna=False):
    """
    Name : Volume-price trend (VPT)
    Reference : https://en.wikipedia.org/wiki/Volume%E2%80%93price_trend
    """
    vpt = volume * ((close - close.shift(1, fill_value=close.mean())) / close.shift(1, fill_value=close.mean()))
    vpt = vpt.shift(1, fill_value=vpt.mean()) + vpt
    if fillna:
        vpt = vpt.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(vpt, name='vpt')
