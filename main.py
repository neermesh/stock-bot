'''
- first run generate_auth_code.py
- it will generate one link
- click on that link
- copy auth code and paste it in auth_code file
- then run generate_token.py
- it will genrate token
- copy this token and paste it in access_token file

'''

import os
import time
import place_order
import threading
from datetime import date
from datetime import timedelta
from fyers_api import fyersModel
from historical_data import live_data
from datetime import datetime


access_token = open("access_token",'r').read()
fyers = fyersModel.FyersModel(client_id='GE5QQJSV08-100', token=access_token, log_path=os.getcwd())
end_date = date.today()
start_date = date.today() - timedelta(days = 1)
call_strike = "NSE:NIFTY23OCT19700PE"
df = live_data(fyers,call_strike,start_date,end_date)
df.to_csv("data.csv")
