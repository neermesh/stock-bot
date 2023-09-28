
import os
from fyers_apiv3 import fyersModel


#access_token = open("access_token",'r').read()
#fyers = fyersModel.FyersModel(client_id='GE5QQJSV08-100', token=access_token, log_path=os.getcwd())
#symbol = "NSE:NIFTY23APR17700CE"


def buy_order(fyers,symbol):
  data = {
      "symbol":symbol,
      "qty":50,
      "type":2,
      "side":1,
      "productType":"BO",
      "limitPrice":0,
      "stopPrice":0,
      "validity":"DAY",
      "disclosedQty":0,
      "offlineOrder":"False",
      "stopLoss":2,
      "takeProfit":4
  }

  response = fyers.place_order(data=data)
  return response

def sell_order(fyers,symbol):
  data = {
      "symbol":symbol,
      "qty":50,
      "type":2,
      "side":-1,
      "productType":"BO",
      "limitPrice":0,
      "stopPrice":0,
      "validity":"DAY",
      "disclosedQty":0,
      "offlineOrder":"False",
      "stopLoss":2,
      "takeProfit":4
  }

  response = fyers.place_order(data=data)
  return response

