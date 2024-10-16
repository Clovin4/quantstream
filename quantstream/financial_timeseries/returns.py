"""basic time series equations"""

import numpy as np

import pandas as pd


# changes over time
def absolute_returns(prices: pd.DataFrame, cumulative: bool) -> pd.Series:
    """
    Calculate the absolute return of a series of prices.

    Args:
        prices (pd.DataFrame): A DataFrame of prices.

    Returns:
        pd.Series: A Series of cumulative returns.
    """
    rets = prices.diff()
    if cumulative:
        return rets.cumsum()
    return rets


def percentage_returns(prices: np.ndarray, cumulative: bool) -> np.ndarray:
    """
    Calculate the percentage return of a series of prices.

    Args:
        prices (pd.DataFrame): A DataFrame of prices.

    Returns:
        pd.Series: A Series of percentage returns.
    """
    rets = prices.pct_change()
    if cumulative:
        return rets.cumsum()
    return rets


def log_returns(prices: np.ndarray, cumulative: bool, normalize: bool) -> np.ndarray:
    """
    Calculate the log return of a series of prices.

    Args:
        prices (pd.DataFrame): A DataFrame of prices.

    Returns:
        pd.Series: A Series of log returns.
    """
    rets = np.log(prices / prices.shift(1))
    if cumulative and normalize:
        return rets.cumsum().apply(np.exp)
    elif cumulative:
        return rets.cumsum()
    return rets


def rolling_statistics():
    pass
