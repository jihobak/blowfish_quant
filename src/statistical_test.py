from statsmodels.tsa.stattools import adfuller


def is_series_stationary(data, p_level=0.05):
    """
    Check if the series is stationary using Augmented Dickey Fuller Test
    (This is usually used for Pairs Trading with spread data)
    
    
    data: pandas.core.series.Series
        1-d data  ex) time series data
    p_level: float
        level of significance required to reject null hypothesis of non-stationarity
    
    returns:
        True if spread can be considered stationary
        False otherwise
    """
    # use the adfuller function to check the spread
    # documentation of function, 'adfuller', http://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html
    adf_result = adfuller(data, autolag='AIC')
    
    # get the p-value
    pvalue = adf_result[1] 
    
    print(f"pvalue {pvalue:.4f}")
    if pvalue <= p_level:
        print(f"pvalue is <= {p_level}, assume data is stationary")
        return True
    else:
        print(f"pvalue is > {p_level}, assume data is not stationary")
        return False
