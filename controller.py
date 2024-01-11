import time
from strategy0001 import Strategy0001


prev_signal = None

while True:
    strategy = Strategy0001("NSE:NIFTY50-INDEX", "5", 5)
    strategy.calculate_moving_averages(20, 50, 1, 2)
    df = strategy.get_data()
    current_signal = df.tail(1)['signal'].values[0]
    print(df.tail(10)[['Open','High','Low','Close','Timestamp2', 'avg', 'avg2', 'signal']])
    if prev_signal is not None and current_signal != prev_signal:
        if current_signal == 1:
            print("Buy signal")
            # place_order('buy', strategy.ticker)
        else:
            print("Sell signal")
            # place_order('sell', strategy.ticker)

    prev_signal = current_signal

    # Sleep for 60 seconds
    time.sleep(3)