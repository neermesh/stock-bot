

import os
import datetime
import pandas as pd


def time_from_datetime(dt):
    if dt.time() < datetime.time(9, 15):
        return datetime.time(9, 15)
    elif dt.time() > datetime.time(15, 30):
        return datetime.time(9, 15)
    else:
        return dt.time()

def live_data(fyers,symbol,start_date,end_date):

    data = {
    "symbol":symbol,
    "resolution":"1",
    "date_format":"1",
    "range_from":start_date,
    "range_to":end_date
    }

    response = fyers.history(data=data)
    df = pd.DataFrame(response['candles'],columns=['Current epoch time','Open','High','Low','Close','volume'])

    # Convert the 'Current epoch time' column to a DatetimeIndex object
    df.index = pd.to_datetime(df['Current epoch time'], unit='s')
    df.index = df.index.tz_localize('UTC').tz_convert('Asia/Kolkata')

    # Create a new column with the date component of the index
    df['Date'] = df.index.date

    # Create a new column with the time component of the index
    df['Time'] = df.index.map(time_from_datetime)
    return df

