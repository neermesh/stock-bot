from fyers_api import fyersModel
from datetime import date
from datetime import timedelta
import os
import pandas as pd
import datetime


def time_from_datetime(dt):
    if dt.time() < datetime.time(9, 15):
        return datetime.time(9, 15)
    elif dt.time() > datetime.time(15, 30):
        return datetime.time(9, 15)
    else:
        return dt.time()

access_token = open("access_token",'r').read()
fyers = fyersModel.FyersModel(client_id='GE5QQJSV08-100', token=access_token, log_path=os.getcwd())
end_date = date.today()
start_date = "2023-12-06"
print(start_date,end_date)
symbol = "NSE:NIFTY50-INDEX"
data = {
    "symbol":symbol,
    "resolution":"1",
    "date_format":"1",
    "range_from":start_date,
    "range_to":end_date
    }

response = fyers.history(data=data)
df = pd.DataFrame(response['candles'],columns=['Current epoch time','Open','High','Low','Close','volume'])

df.index = pd.to_datetime(df['Current epoch time'], unit='s')
df.index = df.index.tz_localize('UTC').tz_convert('Asia/Kolkata')

    # Create a new column with the date component of the index
df['Date'] = df.index.date

    # Create a new column with the time component of the index
df['Time'] = df.index.map(time_from_datetime)

    # Create a new column with the time component of the index

df.to_csv("data.csv")