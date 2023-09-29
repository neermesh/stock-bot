import pandas as pd
import numpy as np

# Define the parameters
ema_fast_period = 50
ema_slow_period = 200
rsi_period = 14
supertrend_period = 14
supertrend_multiplier = 3

# Load historical price data (replace this with your data)
# Sample data structure: Date, Open, High, Low, Close
data = pd.read_csv('data.csv')
#data['Date'] = pd.to_datetime(data['Date'])
#data.set_index('Date', inplace=True)

# Calculate EMA indicators
data['EMA_fast'] = data['Close'].rolling(window=ema_fast_period).mean()
data['EMA_slow'] = data['Close'].rolling(window=ema_slow_period).mean()

# Calculate RSI
delta = data['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
average_gain = gain.rolling(window=rsi_period).mean()
average_loss = loss.rolling(window=rsi_period).mean()
rs = average_gain / average_loss
data['RSI'] = 100 - (100 / (1 + rs))

# Calculate Supertrend
data['TR'] = np.max([
    data['High'] - data['Low'],
    abs(data['High'] - data['Close'].shift(1)),
    abs(data['Low'] - data['Close'].shift(1))
], axis=0)

data['ATR'] = data['TR'].rolling(window=supertrend_period).mean()
data['Upper_band'] = data['High'] - (supertrend_multiplier * data['ATR'])
data['Lower_band'] = data['Low'] + (supertrend_multiplier * data['ATR'])

# Initialize trading signals
data['Buy_Signal'] = 0
data['Sell_Signal'] = 0

# Generate trading signals
import numpy as np

# Calculate the buy and sell signals.
buy_signals = np.where(
    (data['Close'] > data['Upper_band'].shift(1)) &
    (data['RSI'] > 30) &
    (data['EMA_fast'] > data['EMA_slow']),
    1,
    0
)
sell_signals = np.where(
    (data['Close'] < data['Lower_band'].shift(1)) &
    (data['RSI'] < 70) &
    (data['EMA_fast'] < data['EMA_slow']),
    -1,
    0
)

# Assign the buy and sell signals to the DataFrame.
data['Buy_Signal'] = buy_signals
data['Sell_Signal'] = sell_signals


# Backtesting: Calculate returns based on trading signals
data['Returns'] = data['Close'].pct_change() * data['Buy_Signal'] - data['Close'].pct_change() * data['Sell_Signal']

# Print the DataFrame with signals and returns
data.to_csv("signal.csv")