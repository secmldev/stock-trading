import pandas as pd
import numpy as np
from mod_backtest_utils.backtest import Strategy
from mod_backtest_utils.backtest import Portfolio



class RSIStrategy(Strategy):
    """
    Requires:
    symbol: A stock symbol on which to form a strategy
    bars: A DataFrame of bars for the above symbol
    period: Look back period for RSI indicator calculation
    
    """
    
    def __init__(self, symbol, bars, period, buy_threshold, sell_threshold):
        self.symbol = symbol
        self.bars = bars
        self.period = period
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        
    def generate_signals(self):
        """
        Returns the DataFrame of symbols containing the signals to go long, short or hold (1, -1, 0)
        """
        # initialize data frame of signals with the date from price data frame
        signals = pd.DataFrame(index=self.bars.index)
        signals['price'] = self.bars['price']
        
        # create rsi values
        # change
        signals['change'] = signals['price'].diff(periods = 1)
        # gain
        signals['gain'] = signals['change']
        signals.loc[signals['gain'] < 0, ['gain']] = 0.0
        # loss
        signals['loss'] = signals['change']
        signals.loc[signals['loss'] > 0, ['loss']] = 0.0
        signals['loss'] = abs(signals['loss'])
        # average gain
        signals['avg_gain'] = signals['gain'].rolling(window = self.period).mean()
        # average loss
        signals['avg_loss'] = signals['loss'].rolling(window= self.period).mean()
        # rs
        signals['rs'] = signals['avg_gain'] / (signals['avg_loss'] + 0.00005)
        # rsi
        signals['rsi'] = 100 - 100 / (1 + signals['rs'])
        
        
        # Create a signal (invested or not invested) 
        # buy signal when rsi values crosses buy_threshold from bottom
        # sell signal when rsi values crosses sell_threshold from top
        signals['buy']= 0.0
        signals['sell']= 0.0
        signals['buy'] = np.where(signals['rsi'] < self.buy_threshold, -1.0, 0.0)
        signals['sell'] = np.where(signals['rsi'] > self.sell_threshold, 1.0, 0.0)
        signals['buy'] = signals['buy'].diff()
        signals['sell'] = signals['sell'].diff()
        signals.loc[signals['buy']==-1.0,['buy']]=0 
        signals.loc[signals['sell']== 1.0,['sell']]=0 
        signals['buy_sell'] = signals['buy'] + signals['sell']
        return signals[['price','buy_sell']]