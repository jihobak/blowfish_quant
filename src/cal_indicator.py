from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def get_hedge_ratio(s1, s2):
    """
    This function is usually used for "Pairs Trading"
    Parameters:
        s1: pandas.core.series.Series
        s2: pandas.core.series.Series
    
    Return:
        hedge_ratio: numpy.float64
    """

    linear_regression = LinearRegression()
    linear_regression.fit(s1.values.reshape(-1,1), s2.values.reshape(-1, 1))

    hedge_ratio = linear_regression.coef_[0][0]
    intercept = linear_regression.intercept_[0]

    print(f"hedge ratio from regression is {hedge_ratio:.4f}, intercept is {intercept:.4f}")

    return hedge_ratio

def get_spread_ratio(s1, s2, plot=False):
    """
    This function is usually used for "Pairs Trading"

    Parameters:
        s1: pandas.core.series.Series
        s2: pandas.core.series.Series
        plot: boolean
    
    Return:
        spread: pandas.core.series.Series
    """
    # get hedge ratio between two time series data
    hedge_ratio = get_hedge_ratio(s1, s2)

    spread = s2 - s1*hedge_ratio

    print(f"Average spread is {spread.mean()}")

    if plot:
        spread.plot()
        plt.axhline(spread.mean(), color='black')
        plt.xlabel('Days')
        plt.legend(['Spread: s2 - hedge_ratio * s1', 'average spread'])
        plt.show()
    
    return spread
