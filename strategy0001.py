import pandas as pd
import numpy as np
from historical import HistoricalData

class Strategy0001:
    def __init__(self, ticker, interval, duration):
        self.ticker = ticker
        self.interval = interval
        self.duration = duration
        self.historical_data = HistoricalData()
        self.df = self.historical_data.getHistorical(self.ticker, self.interval, self.duration)

    def calculate_moving_averages(self, len, len2, atype, atype2):
        if atype == 1:
            self.df['avg'] = self.df['Close'].rolling(window=len).mean()
        elif atype == 2:
            self.df['avg'] = self.df['Close'].ewm(span=len, adjust=False).mean()
        elif atype == 3:
            self.df['avg'] = self.df['Close'].rolling(window=len).apply(lambda x: np.average(x, weights=np.arange(len, 0, -1)))

        if atype2 == 1:
            self.df['avg2'] = self.df['Close'].rolling(window=len2).mean()
        elif atype2 == 2:
            self.df['avg2'] = self.df['Close'].ewm(span=len2, adjust=False).mean()
        elif atype2 == 3:
            self.df['avg2'] = self.df['Close'].rolling(window=len2).apply(lambda x: np.average(x, weights=np.arange(len2, 0, -1)))

        self.df['signal'] = np.where(self.df['avg2'] > self.df['avg2'].shift(1), 1, 0)

    def save_to_csv(self, filename):
        self.df.to_csv(filename, index=False)

if __name__ == "__main__":
    strategy = Strategy0001("NSE:NIFTY50-INDEX", "1", 5)
    strategy.calculate_moving_averages(20, 50, 1, 2)
    strategy.save_to_csv('data.csv')