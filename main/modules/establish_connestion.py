#! /usr/bin/env python3

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

class TradingApp(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId, errorCode, errorCode))

app = TradingApp()
app.connect('127.0.0.1', 4002, clientId=1)
