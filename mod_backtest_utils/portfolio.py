from mod_backtest_utils.backtest import Portfolio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MarketOnPricePortfolio(Portfolio):
    """
    Inherits Portfolio to create a system that purchases 100 units of a particular symbol upon a long/short signals, 
    assuming the market open price of a bar.
    Encapsulates the notion of a portfolio of positions based on a set of signals as provided by a Strategy
    
    In addition, there are zero transaction costs and cash can be immediately borrowed for shorting (no margin posting or interest
    requirements).
    
    Requires:
    symbol - A stock symbol which forms the basis of the portfolio.
    signals - A pandas DataFrame of signals (1, 0, -1) or each symbol.
    Initial_capital - the amount in cash at the start of the portfolio."""
    
    def __init__(self, symbol, signals, initial_capital=100000.0):
        self.symbol = symbol
        self.signals = signals
        self.initial_capital = float(initial_capital)
        self.positions = self.generate_positions()
        self.portfolio = self.backtest_portfolio()
        
    def generate_positions(self):
        """
        Creates a 'positions' DataFrame that simply longs or shorts 100 of the particular symbol based on the 
        forecast signals of {1, 0, -1} from the signals DataFrame."""
        positions = pd.DataFrame(index= self.signals.index).fillna(0.0)
        # Buy and sell a 100 shares based on signals and accumulate position
        positions[self.symbol] = 100 * self.signals['buy_sell'].cumsum() 
        return positions
    
    def backtest_portfolio(self):
        """
        Constructs a portfolio from the positions DataFrame by assuming the ability to trade at 
        the precise market price of each bar.
        
        Calculates the total of cash and the holding (market price of each position per bar), in order to 
        generate an equity curve (total) and a set of bar based returns ('return).
        
        Returns the portfolio object to be used elsewhere.
        """
        
        # Construct the portfolio dataframe to use the same index
        # as 'positons' and with a set of 'trading orders' in the
        # 'pos_diff' object, assumping market open prices.
        
        portfolio = pd.DataFrame(index=self.signals.index)
        # Initialize the portfolio with value owned 
        portfolio[self.symbol] = self.positions[self.symbol].multiply(self.signals['price'], axis=0)
        pos_diff = 100 * self.signals[['buy_sell']]
        # add holding to portfolio
        portfolio['holdings'] = (self.positions.multiply(self.signals['price'], axis=0)).sum(axis=1)
        # Add `cash` to portfolio
        portfolio['cash'] = self.initial_capital - (pos_diff.multiply(self.signals['price'], axis=0)).sum(axis=1).cumsum()   
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        # return the portfolio
        return portfolio[['holdings', 'cash', 'total']]
    
    
    def plot_stock_portfolio(self):
        """
        Plot portfolio developed using buy and sell signal
        """
        fig = plt.figure(figsize=(20,20))
        ax1 = fig.add_subplot(411)
        self.portfolio['holdings'].plot(ax=ax1, title = "Stock Holiding Value")
        ax2 = fig.add_subplot(412)
        self.portfolio['cash'].plot(ax=ax2, title = "Cash")
        ax3 = fig.add_subplot(413)
        self.portfolio['total'].plot(ax=ax3, title = "Total")
        plt.show()