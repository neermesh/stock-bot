import pandas as pd

# Sample stock data with Buy_Signal column


df = pd.read_csv("signal.csv")

# Initialize variables
holdings = 0  # Number of stocks currently held
total_pnl = 0  # Total Profit & Loss
buy_price = None

# Calculate P&L based on buy signals
for index, row in df.iterrows():
    if row['Buy_Signal'] == 1:
        # Buy the stock
        buy_price = row['Open']
        holdings += 1
    elif holdings > 0:
        # Sell the stock if we have holdings and it's not a buy signal
        sell_price = row['Close']
        pnl = (sell_price - buy_price) * holdings
        total_pnl += pnl
        holdings = 0  # Reset holdings to 0

# If there are remaining holdings at the end, calculate their P&L
if holdings > 0:
    last_close_price = df.iloc[-1]['Close']
    total_pnl += (last_close_price - buy_price) * holdings

print("Total P&L: ${:.2f}".format(total_pnl))
