import numpy as np
import pandas as pd

from .utils import *

def rsi(close, n=14, fillna=False):
    """
    Name : Relative Strength Index (RSI)
    Reference : https://www.investopedia.com/terms/r/rsi.asp
    """
    diff = close.diff(1)
    which_dn = diff < 0

    up, dn = diff, diff*0
    up[which_dn], dn[which_dn] = 0, -up[which_dn]

    emaup = ema(up, n, fillna)
    emadn = ema(dn, n, fillna)

    rsi = 100 * emaup / (emaup + emadn)
    if fillna:
        rsi = rsi.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(rsi, name='rsi')

def tsi(close, r=25, s=13, fillna=False):
    """
    Name : True strength index (TSI)
    Reference : https://en.wikipedia.org/wiki/True_strength_index
    """
    m = close - close.shift(1, fill_value=close.mean())
    m1 = m.ewm(r).mean().ewm(s).mean()
    m2 = abs(m).ewm(r).mean().ewm(s).mean()
    tsi = m1 / m2
    tsi *= 100
    if fillna:
        tsi = tsi.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(tsi, name='tsi')

def sto_osci(high, low, close, n=14, fillna=False):
    """
    Name : Stochastic Oscillator
    Reference : https://www.investopedia.com/terms/s/stochasticoscillator.asp
    """
    smin = low.rolling(n, min_periods=0).min()
    smax = high.rolling(n, min_periods=0).max()
    stoch_k = 100 * (close - smin) / (smax - smin)

    if fillna:
        stoch_k = stoch_k.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(stoch_k, name='stoch_k')


def kama(close, n=10, pow1=2, pow2=30, fillna=False):
    """
    Name : Kaufman's Adaptive Moving Average (KAMA)
    Reference : https://www.tradingview.com/ideas/kama/
    """
    close_values = close.values
    vol = pd.Series(abs(close - np.roll(close, 1)))

    ER_num = abs(close_values - np.roll(close_values, n) )
    ER_den = vol.rolling(n).sum()
    ER = ER_num / ER_den

    sc = (( ER*(2.0/(pow1+1)-2.0/(pow2+1.0))+2/(pow2+1.0) ) ** 2.0).values

    kama = np.zeros(sc.size)
    N = len(kama)
    first_value = True

    for i in range(N):
        if np.isnan(sc[i]):
            kama[i] = np.nan
        else:
            if first_value:
                kama[i] = close_values[i]
                first_value = False
            else:
                kama[i] = kama[i-1] + sc[i] * (close_values[i] - kama[i-1])

    kama = pd.Series(kama, name='kama', index=close.index)

    if fillna:
        kama = kama.replace([np.inf, -np.inf], np.nan).fillna(close)

    return kama

