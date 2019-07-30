import numpy as np
import pandas as pd

from .utils import *


def macd(close, n_fast=12, n_slow=26, fillna=False):
    """
    Name : Moving Average Convergence Divergence (MACD)
    Reference : https://en.wikipedia.org/wiki/MACD
    """
    emafast = ema(close, n_fast, fillna)
    emaslow = ema(close, n_slow, fillna)
    macd = emafast - emaslow
    if fillna:
        macd = macd.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(macd, name='MACD_%d_%d' % (n_fast, n_slow))


def macd_signal(close, n_fast=12, n_slow=26, n_sign=9, fillna=False):
    """
    Name : Moving Average Convergence Divergence (MACD Signal)
    Reference : https://en.wikipedia.org/wiki/MACD
    """
    emafast = ema(close, n_fast, fillna)
    emaslow = ema(close, n_slow, fillna)
    macd = emafast - emaslow
    macd_signal = ema(macd, n_sign, fillna)
    if fillna:
        macd_signal = macd_signal.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(macd_signal, name='MACD_sign')

def trix(close, n=15, fillna=False):
    """
    Name : Trix (TRIX)
    Reference : http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix
    """
    ema1 = ema(close, n, fillna)
    ema2 = ema(ema1, n, fillna)
    ema3 = ema(ema2, n, fillna)
    trix = (ema3 - ema3.shift(1, fill_value=ema3.mean())) / ema3.shift(1, fill_value=ema3.mean())
    trix *= 100
    if fillna:
        trix = trix.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(trix, name='trix_'+str(n))

def aroon_up(close, n=25, fillna=False):
    """
    Name : Aroon Indicator (AI)
    Identify when trends are likely to change direction (uptrend).
    Aroon Up - ((N - Days Since N-day High) / N) x 100
    Reference : https://www.investopedia.com/terms/a/aroon.asp
    """
    aroon_up = close.rolling(n, min_periods=0).apply(lambda x: float(np.argmax(x) + 1) / n * 100, raw=True)
    if fillna:
        aroon_up = aroon_up.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(aroon_up, name='aroon_up'+str(n))

def aroon_down(close, n=25, fillna=False):
    """
    Name : Aroon Indicator (AI)
    Identify when trends are likely to change direction (downtrend).
    Aroon Down - ((N - Days Since N-day Low) / N) x 100
    Reference : https://www.investopedia.com/terms/a/aroon.asp
    """
    aroon_down = close.rolling(n, min_periods=0).apply(lambda x: float(np.argmin(x) + 1) / n * 100, raw=True)
    if fillna:
        aroon_down = aroon_down.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(aroon_down, name='aroon_down'+str(n))
