from mod_backtest_utils.backtest import Strategy
from mod_backtest_utils.backtest import Portfolio
import pandas as pd
import numpy as np

class ROCStrategy(Strategy):
    """
    Requires:
    symbol: A stock symbol on which to form a strategy
    bars: A DataFrame of bars for the above symbol
    period: Lookback period for roc calculation
    """
    
    def __init__(self, symbol, bars, period, buy_threshold, sell_threshold):
        self.symbol = symbol
        self.bars = bars
        self.period = period
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
 
    def generate_signals(self):
        """
        Returns the DataFrame of signal containing the signals to go long, short or hold (1, -1, 0)
        """
        # initiate signal data frame with date as index
        signals = pd.DataFrame(index=self.bars.index)
        signals['price'] = self.bars['price']
        
        # calculate roc values for the given period
        signals['roc' + str(self.period)] = signals['price'].diff(periods=self.period) / signals['price'].shift(periods=self.period)
        
        # buy sell signal generations
        signals['buy']= 0.0
        signals['sell']= 0.0
        signals['buy'] = np.where(signals['roc' + str(self.period)] < self.buy_threshold, -1.0, 0.0)
        signals['sell'] = np.where(signals['roc' + str(self.period)] > self.sell_threshold, 1.0, 0.0)
        signals['buy'] = signals['buy'].diff()
        signals['sell'] = signals['sell'].diff()
        signals.loc[signals['buy']==-1.0,['buy']] = 0.0 
        signals.loc[signals['sell']== 1.0,['sell']] = 0.0 
        signals['buy_sell'] = signals['buy'] + signals['sell']
        return signals[['price', 'buy_sell']]