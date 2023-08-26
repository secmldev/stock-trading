import pandas as pd
import numpy as np
from mod_backtest_utils.backtest import *

class BBStrategy(Strategy):
    """
    Requires:
    symbol: A stock symbol on which to form a strategy
    bars: A DataFrame of bars for the above symbol
    period: Look back period for BB indicator calculation
    stdmultiplier: the parameter to generate upper and lower band
    
    """
    
    def __init__(self, symbol, bars, period, stdmultiplier):
        self.symbol = symbol
        self.bars = bars
        self.period = period
        self.stdmultiplier = stdmultiplier
        
    def generate_signals(self):
        """
        Returns the DataFrame of symbols containing the signals to go long, short or hold (1, -1, 0)
        """
        # initialize data frame of signals with the date from price data frame
        signals = pd.DataFrame(index=self.bars.index)
        signals['price'] = self.bars['price']
        
        # create bb value
        signals['middleband'] = signals['price'].rolling(window=self.period).mean()
        signals['upperband'] = signals['middleband'] + self.stdmultiplier * (signals['price'].rolling(window= self.period).std())
        signals['lowerband'] = signals['middleband'] - self.stdmultiplier * (signals['price'].rolling(window= self.period).std())

        # Create a signal (invested or not invested) 
        # buy signal when rsi values crosses buy_threshold from bottom
        # sell signal when rsi values crosses sell_threshold from top
        signals['sell']= 0.0
        signals['buy']= 0.0
        signals['buy'][self.period:] = np.where(signals['price'][self.period:] < signals['lowerband'][self.period:], -1.0, 0.0)
        signals['sell'][self.period:] = np.where(signals['price'][self.period:] > signals['upperband'][self.period:],1.0,0)
        signals['buy'] = signals['buy'].diff()
        signals['sell'] = signals['sell'].diff()
        signals.loc[signals['buy'] == -1.0,['buy']]=0 
        signals.loc[signals['sell'] == 1.0,['sell']]=0 
        signals['buy_sell'] = signals['buy'] + signals['sell']
        return signals[['price', 'buy_sell']]