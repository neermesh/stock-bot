import os
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
from fyers_apiv3 import fyersModel
from datetime import datetime
import argparse


class StockBot:
    def __init__(self, stock="NIFTY", otm=100, SL_point=10):
        self.stock = stock
        self.otm = otm
        self.SL_point = SL_point
        self.access_token = open("access_token",'r').read()
        self.fyers = fyersModel.FyersModel(client_id='GE5QQJSV08-100', token=self.access_token, log_path=os.getcwd())

    def getIndexSpot(self):
        if self.stock == "BANKNIFTY":
            return "NSE:NIFTYBANK-INDEX"
        elif self.stock == "NIFTY":
            return "NSE:NIFTY50-INDEX"

    def getNiftyExpiryDate(self):
        import datetime
        nifty_expiry = {
            datetime.date(2023, 12, 28): "23DEC",
            datetime.date(2024, 1, 4): "24104",
            datetime.date(2024, 1, 11): "24111",
            datetime.date(2024, 1, 18): "24118",
            datetime.date(2024, 1, 25): "24JAN",
        }
        today = datetime.date.today()
        for date_key, value in nifty_expiry.items():
            if today <= date_key:
                return value

    def getBankNiftyExpiryDate(self):
        import datetime
        banknifty_expiry = {
            datetime.date(2023, 12, 28): "23DEC",
            datetime.date(2024, 1, 3): "24103",
            datetime.date(2024, 1, 10): "24110",
            datetime.date(2024, 1, 17): "24117",
            datetime.date(2024, 1, 25): "24JAN",
        }
        today = datetime.date.today()
        for date_key, value in banknifty_expiry.items():
            if today <= date_key:
                return value

    def getOptionFormat(self, intExpiry, strike, ce_pe):
        return "NSE:" + str(self.stock) + str(intExpiry)+str(strike)+str(ce_pe)

    def findStrikePriceATM(self):
        if self.stock == "BANKNIFTY":
            intExpiry=self.getBankNiftyExpiryDate()
        elif self.stock == "NIFTY":
            intExpiry=self.getNiftyExpiryDate()
        print(intExpiry)
        data = {"symbols": self.getIndexSpot()}
        ltp = self.fyers.quotes(data=data)
        ltp = ltp['d'][0]['v']['lp']
        print("current pointer : ",ltp)
        if self.stock == "BANKNIFTY":
            closest_Strike = int(round((ltp / 100),0) * 100)
        elif self.stock == "NIFTY":
            closest_Strike = int(round((ltp / 50),0) * 50)
        print("closest strike : ",closest_Strike)
        closest_Strike_CE = closest_Strike+self.otm
        closest_Strike_PE = closest_Strike-self.otm
        print("closest Strike CE : ",closest_Strike_CE)
        print('closest Strike PE : ',closest_Strike_PE)
        atmCE = self.getOptionFormat(intExpiry, closest_Strike_CE, "CE")
        atmPE = self.getOptionFormat(intExpiry, closest_Strike_PE, "PE")
        return {"atmCE":atmCE,"atmPE":atmPE}
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process stock input.')
    parser.add_argument('--stock', type=str, help='The stock to process')

    args = parser.parse_args()

    bot = StockBot(args.stock)
    strike_price = bot.findStrikePriceATM()
    print(strike_price)