from backtesting import Backtest, Strategy
import pandas as pd

def calculate_ema(data, window):
    return pd.Series(data).ewm(span=window).mean()

class EMACross(Strategy):
    short_window = 10
    long_window = 50

    def init(self):
        self.short_ema = self.I(calculate_ema, self.data.Close, self.short_window)
        self.long_ema = self.I(calculate_ema, self.data.Close, self.long_window)

    def next(self):
        if not self.position:  # if not in the market
            if self.short_ema[-1] > self.long_ema[-1]:
                self.buy()
        else:  # in the market
            if self.short_ema[-1] < self.long_ema[-1]:
                self.sell()

# Load data
data = pd.read_csv('data.csv', index_col='Date', parse_dates=True)

# Remove duplicates
data = data.loc[~data.index.duplicated(keep='first')]

# Create a Backtest instance
# ... (previous code)

# Create a Backtest instance
bt = Backtest(data, EMACross, cash=100000, commission=.002)

# Run the backtest
stats = bt.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % stats['Equity Final [$]'])

# Print the statistics
print('Stats:', stats)

'''# Optimize the strategy
stats = bt.optimize(short_window=range(1, 15, 1),
                    long_window=range(5, 60, 5),
                    maximize='Equity Final [$]',
                    constraint=lambda p: p.short_window < p.long_window)

# Print out the final result
print('Final Portfolio Value: %.2f' % stats['Equity Final [$]'])

# Print the optimized parameters
print('Optimized Parameters:', stats['_strategy'])'''