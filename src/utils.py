import pandas as pd
import numpy as np


def get_most_volatile(prices):
    """Return the ticker symbol for the most volatile stock.
    
    Parameters
    ----------
    prices : pandas.DataFrame
        a pandas.DataFrame object with columns: ['ticker', 'date', 'price']
    
    Returns
    -------
    ticker : string
        ticker symbol for the most volatile stock
    """
    stds = prices.groupby(['ticker']).std()
    return np.argmax(stds['price'])


def calculate_simple_moving_average(rolling_window, close):
    """
    Compute the simple moving average.
    
    Parameters
    ----------
    rolling_window: int
        Rolling window length
    close : DataFrame
        Close prices for each ticker and date
    
    Returns
    -------
    simple_moving_average : DataFrame
        Simple moving average for each ticker and date
    """
    # TODO: Implement Function
    
    return close.rolling(rolling_window).mean()