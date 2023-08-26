# ma_cross.py

from mod_backtest_utils.backtest import Strategy
from mod_backtest_utils.backtest import Portfolio
import pandas as pd
import numpy as np

class MovingAverageCrossStrategy(Strategy):
    """
    Requires:
    symbol: A stock symbol on which to form a strategy
    bars: A DataFrame of bars for the above symbol
    short_window: Looback period for short moving average
    long_window: Lookback period for long movign average.
    """
    
    def __init__(self, symbol, bars, short_window= 80, long_window= 100, signal_window = 20):
        self.symbol = symbol
        self.bars = bars
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        
    def generate_signals(self):
        """
        Returns the DataFrame of symbols containing the signals to go long, short or hold (1, -1, 0)
        """
        signals = pd.DataFrame(index=self.bars.index)
        signals['buy_sell'] = 0.0
        signals['price'] = self.bars['price']
        
        # Create the set of short and long simple moving average over the respective periods
        signals['SMA'] = signals['price'].rolling(self.short_window, min_periods=1).mean()
        signals['LMA'] = signals['price'].rolling(self.long_window, min_periods=1).mean()
        
        # Create a signal (invested or not invested) when the short moving average cross the 
        # long moving average, but only for the period greater than the long moving average window
        signals['buy_sell'][self.long_window:] = np.where(signals['SMA'][self.long_window:]
                                                        > signals['LMA'][self.long_window:], 1.0, 0.0)
        
        # Take the difference of the signals in order to generate actual trading orders
        signals['buy_sell'] = signals['buy_sell'].diff()
        
        return signals[['price', 'buy_sell']]
        

