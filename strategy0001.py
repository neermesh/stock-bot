import pandas as pd
import numpy as np

# Assuming 'df' is your DataFrame and it has 'Close' column
df = pd.read_csv('data.csv')

# Moving Average Length - LookBack Period
len = 20
len2 = 50

# 1=SMA, 2=EMA, 3=WMA
atype = 1
atype2 = 2

# Calculate moving averages
if atype == 1:
    df['avg'] = df['Close'].rolling(window=len).mean()
elif atype == 2:
    df['avg'] = df['Close'].ewm(span=len, adjust=False).mean()
elif atype == 3:
    df['avg'] = df['Close'].rolling(window=len).apply(lambda x: np.average(x, weights=np.arange(len, 0, -1)))

if atype2 == 1:
    df['avg2'] = df['Close'].rolling(window=len2).mean()
elif atype2 == 2:
    df['avg2'] = df['Close'].ewm(span=len2, adjust=False).mean()
elif atype2 == 3:
    df['avg2'] = df['Close'].rolling(window=len2).apply(lambda x: np.average(x, weights=np.arange(len2, 0, -1)))

# Change color based on direction
#df['color'] = np.where(df['avg'] > df['avg'].shift(1), 'lime', 'red')
df['signal'] = np.where(df['avg2'] > df['avg2'].shift(1), 1, 0)

df.to_csv('data1.csv', index=False)