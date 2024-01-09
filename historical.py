import os
import pandas as pd
import datetime
import pytz
import argparse
from fyers_apiv3 import fyersModel

class HistoricalData:
    def __init__(self, client_id='GE5QQJSV08-100'):
        self.access_token = open("access_token",'r').read()
        self.fyers = fyersModel.FyersModel(client_id=client_id, token=self.access_token, log_path=os.getcwd())



    def getHistorical(self, ticker, interval, duration):
        range_from = datetime.datetime.today()-datetime.timedelta(duration)
        range_to = datetime.datetime.today()

        from_date_string = range_from.strftime("%Y-%m-%d")
        to_date_string = range_to.strftime("%Y-%m-%d")
        data = {
            "symbol":ticker,
            "resolution":interval,
            "date_format":"1",
            "range_from":from_date_string,
            "range_to":to_date_string,
            "cont_flag":"1"
        }

        response = self.fyers.history(data=data)['candles']

        # Create a DataFrame
        columns = ['Timestamp','Open','High','Low','Close','Volume']
        df = pd.DataFrame(response, columns=columns)

        # Convert Timestamp to datetime in UTC
        df['Timestamp2'] = pd.to_datetime(df['Timestamp'],unit='s').dt.tz_localize(pytz.utc)

        # Convert Timestamp to IST
        ist = pytz.timezone('Asia/Kolkata')
        df['Timestamp2'] = df['Timestamp2'].dt.tz_convert(ist)
        # Filter rows where 'Timestamp2' is less than 15:30
        filtered_df = df[df['Timestamp2'].dt.time < pd.to_datetime('15:30').time()]

        return filtered_df
    





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process stock input.')
    parser.add_argument('--ticker', type=str, help='The ticker to process')
    parser.add_argument('--interval', type=str, help='The interval to process')
    parser.add_argument('--duration', type=int, help='The duration to process')

    args = parser.parse_args()

    historical_data = HistoricalData()
    df = historical_data.getHistorical(args.ticker, args.interval, args.duration)
    print(df)