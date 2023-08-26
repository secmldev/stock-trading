from mod_backtest_utils.backtest import Strategy
# from backtest import Strategy, Portfolio
import pandas as pd
import numpy as np


# random_forecast.py

class RandomForecastingStrategy(Strategy):
    """
    Derives from strategy to produce a set of signals that are randomly generated long/shorts. 
    Clearly a nonsensical strategy, but perfectly acceptable for demonstrating the backtesting infrastructure!
    """
    
    def __init__(self, symbol, bars):
        """
        requires 
        symbol: name of the stock
        bars: stock price
        """
        self.symbol = symbol
        self.bars = bars
        
    def generate_signals(self):
        """
        Creates a pandas DataFrame of random signals.
        """
        
        signals = pd.DataFrame(index = self.bars.index)
        signals['price'] = self.bars['price']
        signals['buy_sell'] = np.sign(np.random.randn(len(signals)))
        
        # The first five elements are set to zero in order to minimise upstream NaN errors in the forecaster.
        signals['buy_sell'][0:5] = 0.0
        return signals[['price', 'buy_sell']]
    
    
