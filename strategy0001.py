import pandas as pd

def calculate_ssl(df, len):
    smaHigh = df['High'].rolling(window=len).mean()
    smaLow = df['Low'].rolling(window=len).mean()

    Hlv = 0
    Hlv_list = [0]
    for i in range(len, len(df)):
        if df['Close'].iloc[i] > smaHigh.iloc[i]:
            Hlv = 1
        elif df['Close'].iloc[i] < smaLow.iloc[i]:
            Hlv = -1
        else:
            Hlv = Hlv_list[-1]
        Hlv_list.append(Hlv)

    df['sslDown'] = pd.Series(Hlv_list) < 0
    df['sslUp'] = pd.Series(Hlv_list) > 0

    df['sslDown'] = df['sslDown'].apply(lambda x: smaHigh if x else smaLow)
    df['sslUp'] = df['sslUp'].apply(lambda x: smaLow if x else smaHigh)
    df['ssl_signal'] = (df['sslDown'] < df['sslUp']).astype(int) - (df['sslDown'] > df['sslUp']).astype(int)
    return df


