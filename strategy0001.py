import pandas as pd
import numpy as np
import pandas_ta as ta
from math import sqrt
from historical import HistoricalData

# Create an instance of HistoricalData
historical_data = HistoricalData()

# Get historical data
df = historical_data.getHistorical('NSE:NIFTY50-INDEX', '5', 5)


useCurrentRes = True
resCustom = 'D'
len1 = 20
factorT3 = 0.7
atype = 1
spc = False
cc = True
smoothe = 2
doma2 = False
spc2 = False
len2 = 50
sfactorT3 = 0.7
atype2 = 1
cc2 = True
warn = False
warn2 = False
sd = False

res = 'period' if useCurrentRes else resCustom


def weighted_moving_average(data, period):
    weights = np.arange(1, period + 1)
    return data.rolling(period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def hull_moving_average(data, period):
    wma_half = weighted_moving_average(data, period // 2)
    wma_full = weighted_moving_average(data, period)
    sqrt_period = int(np.sqrt(period))
    return weighted_moving_average(2 * wma_half - wma_full, sqrt_period)


# Calculate Hull Moving Average
df['HMA'] = hull_moving_average(df['Close'], len1)

def triple_exponential_moving_average(data, period):
    ema1 = data.ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()
    ema3 = ema2.ewm(span=period, adjust=False).mean()
    return 3 * (ema1 - ema2) + ema3

# Calculate Triple Exponential Moving Average
df['TEMA'] = triple_exponential_moving_average(df['Close'], len1)

# Print DataFrame
print(df)



# Assuming 'df' is your DataFrame and 'Close' is the column with closing prices
src = df['Close']

# Define the length and factor
len = 14  # replace with desired length
factorT3 = 0.7  # replace with desired factor
factor = factorT3 * 0.10

# Define the gd function
def gd(src, len, factor):
    ema1 = src.ewm(span=len, adjust=False).mean()
    ema2 = ema1.ewm(span=len, adjust=False).mean()
    return ema1 * (1 + factor) - ema2 * factor

# Define the t3 function
def t3(src, len, factor):
    return gd(gd(gd(src, len, factor), len, factor), len, factor)

# Calculate Tilson T3
df['TilsonT3'] = t3(src, len, factor)



# Define the length and atype
len = 14  # replace with desired length
len2 = 28  # replace with desired length for second MA
atype = 1  # replace with desired atype

# Define the moving averages
def sma(src, len):
    return src.rolling(window=len).mean()

def ema(src, len):
    return src.ewm(span=len, adjust=False).mean()

def wma(src, len):
    weights = np.arange(1, len + 1)
    return src.rolling(window=len).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def hullma(src, len):
    return wma(2 * wma(src, len // 2) - wma(src, len), round(sqrt(len)))

def vwma(src, len):
    volume = df['Volume']  # replace with your volume column
    return src.mul(volume).rolling(window=len).sum() / volume.rolling(window=len).sum()

def rma(src, len):
    return src.ewm(alpha=1/len, adjust=False).mean()

# Calculate the chosen moving average
if atype == 1:
    avg = sma(src, len)
elif atype == 2:
    avg = ema(src, len)
elif atype == 3:
    avg = wma(src, len)
elif atype == 4:
    avg = hullma(src, len)
elif atype == 5:
    avg = vwma(src, len)
elif atype == 6:
    avg = rma(src, len)
elif atype == 7:
    ema1 = ema(src, len)
    ema2 = ema(ema1, len)
    ema3 = ema(ema2, len)
    avg = 3 * (ema1 - ema2) + ema3
else:
    avg = df['TilsonT3']  # assuming Tilson T3 is already calculated and stored in the DataFrame

# Calculate the second moving averages
hullma2 = wma(2 * wma(src, len2 // 2) - wma(src, len2), round(sqrt(len2)))

sema1 = ema(src, len2)
sema2 = ema(sema1, len2)
sema3 = ema(sema2, len2)
stema = 3 * (sema1 - sema2) + sema3


sfactor = sfactorT3 * 0.10

# Define the sgd function
def sgd(src, len2, sfactor):
    ema1 = src.ewm(span=len2, adjust=False).mean()
    ema2 = ema1.ewm(span=len2, adjust=False).mean()
    return ema1 * (1 + sfactor) - ema2 * sfactor

# Define the st3 function
def st3(src, len2, sfactor):
    return sgd(sgd(sgd(src, len2, sfactor), len2, sfactor), len2, sfactor)

# Calculate second Tilson T3
df['SecondTilsonT3'] = st3(src, len2, sfactor)

# Define the atype2
atype2 = 1  # replace with desired atype for second MA

# Calculate the second chosen moving average
if atype2 == 1:
    avg2 = sma(src, len2)
elif atype2 == 2:
    avg2 = ema(src, len2)
elif atype2 == 3:
    avg2 = wma(src, len2)
elif atype2 == 4:
    avg2 = hullma2
elif atype2 == 5:
    avg2 = vwma(src, len2)
elif atype2 == 6:
    avg2 = rma(src, len2)
elif atype2 == 7:
    sema1 = ema(src, len2)
    sema2 = ema(sema1, len2)
    sema3 = ema(sema2, len2)
    avg2 = 3 * (sema1 - sema2) + sema3
else:
    avg2 = df['SecondTilsonT3']  # assuming second Tilson T3 is already calculated and stored in the DataFrame

# Assign the moving averages to out and out_two
out = avg
out_two = avg2

# In Pine Script, the security function is used to get data from a different symbol or timeframe.
# In Python, you would need to handle this manually by getting the data for the desired symbol or timeframe before the calculations.
# The following lines are placeholders and should be replaced with your actual implementation.
tickerid = 'AAPL'  # replace with your ticker symbol
res = '1D'  # replace with your resolution
out1 = out
out2 = out_two

# Assuming 'Open' and 'Close' are columns in your DataFrame with opening and closing prices
open = df['Open']
close = df['Close']

# Calculate the conditions for price crossing the moving averages
cr_up = (open < out1) & (close > out1)
cr_down = (open > out1) & (close < out1)
cr_up2 = (open < out2) & (close > out2)
cr_down2 = (open > out2) & (close < out2)

# Define the functions for bar color criteria
def iscrossup():
    return cr_up

def iscrossdown():
    return cr_down

def iscrossup2():
    return cr_up2

def iscrossdown2():
    return cr_down2

import matplotlib.pyplot as plt

# Define the smoothe and cc
smoothe = 1  # replace with desired smoothe
cc = True  # replace with desired cc
cc2 = True  # replace with desired cc2

# Calculate the conditions for moving average up and down
ma_up = out1 >= out1.shift(smoothe)
ma_down = out1 < out1.shift(smoothe)

# Define the colors
# Add 'col' and 'col2' to the DataFrame
df['col'] = pd.Series(np.where(ma_up, 'lime', np.where(ma_down, 'red', 'aqua')), index=out1.index)
df['col2'] = pd.Series(np.where(ma_up, 'lime', np.where(ma_down, 'red', 'white')), index=out1.index)

# Define the circleYPosition
circleYPosition = out2

# Plot the moving averages
plt.figure(figsize=(14, 7))
plt.plot(out1, label="Multi-Timeframe Moving Avg", linewidth=2, color=df['col'])
plt.plot(out2 if doma2 else np.nan, 'o', label="2nd Multi-TimeFrame Moving Average", markersize=4, color=df['col2'])
plt.plot(circleYPosition if sd and out1.cross(out2) else np.nan, 'x', markersize=10, color='aqua')
# Add the bar colors for price crossing the moving averages
# In Python, you would need to handle this manually by creating a bar plot with the desired colors.
# The following lines are placeholders and should be replaced with your actual implementation.
spc = True  # replace with desired spc
spc2 = True  # replace with desired spc2
bar_colors = ['yellow' if (spc and is_crossup) or (spc2 and is_crossup2) else 'blue' for is_crossup, is_crossup2 in zip(iscrossup(), iscrossup2())]
plt.bar(df.index, close, color=bar_colors)
df.to_csv('output.csv')
plt.legend()
plt.show()