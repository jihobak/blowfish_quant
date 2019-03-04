import pandas as pd
import numpy as np


def covariance_matrix(returns):
    """
    Takes the return series of a set of stocks
    and calculates the covariance matrix.
    
    Parameters
    ----------
    returns : numpy.ndarray
        2D array containing stock return series in each row.
                
    Returns
    -------
    x : np.ndarray
        A numpy ndarray containing the covariance matrix
    """
    
    #covariance matrix of returns
    cov = np.cov(returns)
        
    return cov


def calculate_arithmetic_rate_of_return(close):
    """
    Compute returns for each ticker and date in close.
    
    Parameters
    ----------
    close : DataFrame
        Close prices for each ticker and date
    
    ex)
                        WVA        WMYT          LUYB         EBAC         QNS
        2000-08-09  21.05081048 17.01384381   10.98450376  11.24809343 12.96171273
        2000-08-10  15.63570259 14.69054309   11.35302769 475.74195118 11.95964043
        2000-08-11 482.34539247 35.20258059 3516.54167823  66.40531433 13.50396048
        2000-08-12  10.91893302 17.90864387   24.80126542  12.48895419 10.52435923
        2000-08-13  10.67597197 12.74940144   11.80525758  21.53903949 19.99766037
        2000-08-14  11.54549538 23.98146843   24.97476306  36.03196210 14.30433232
    
    Returns
    -------
    arithmnetic_returns : Series
        arithmnetic_returns at the end of the period for each ticker
    
    """
    returns = (close/close.shift(1))-1
    cumsum_returns = returns.cumsum(axis =0)
    sum_of_returns = cumsum_returns.iloc[-1] 
    
    mean_returns = sum_of_returns/returns.shape[0]
    
    return mean_returns


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


def estimate_volatility(prices, l):
    """Create an exponential moving average model of the volatility of a stock
    log return, and return the most recent (last) volatility estimate.
    
    Parameters
    ----------
    prices : pandas.Series
        A series of adjusted closing prices for a stock.
        
    l : float
        The 'lambda' parameter of the exponential moving average model. Making
        this value smaller will cause the model to weight older terms less 
        relative to more recent terms.
        
    Returns
    -------
    last_vol : float
        The last element of your exponential moving averge volatility model series.
    
    """
    log_return = np.log(prices).diff(1)
    squared_log_return = np.square(log_return)  
    ewms = squared_log_return.ewm(alpha=1-l).mean()
    
    return np.sqrt(ewms.values[-1])