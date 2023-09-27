import os
from fyers_api import fyersModel

access_token = open("access_token",'r').read()
fyers = fyersModel.FyersModel(client_id='GE5QQJSV08-100', token=access_token, log_path=os.getcwd())

response = fyers.funds()
print(response)