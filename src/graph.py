import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.style.use(['dark_background'])

def plot_candles(prices, filename='sample_graph', save=''):
    """
    Plots a candlestick chart for trainning Neural Networks.
    
    Parameters:
        prices: pandas.DataFrame
            a pandas.DataFrame object with columns such as 'open', 'close', 'high', 'low' and volume
        filename: str
            filename for save
        save: boolean
            save or not
    
    Returns:
        None
    """
    open_price = prices['Open']
    close_price = prices['Close']
    low = prices['Low']
    high = prices['High']
    
    bottom = pd.concat([open_price, close_price], axis=1).min(axis=1)
    top = pd.concat([open_price, close_price], axis=1).max(axis=1)
    
    fig, ax = plt.subplots(1, 1, figsize=(3,3))
    
    x = np.arange(len(prices))
    candle_colors = [ 'r' if condition else 'g' for condition in open_price > close_price]
    candles = ax.bar(x, top-bottom, bottom=bottom, color=candle_colors, linewidth=0)
    lines = ax.vlines(x, low, high, color=candle_colors, linewidth=1)
    
    ax.axis('off')
    
    plt.savefig(filename,dpi=100)