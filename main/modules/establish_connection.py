#! /usr/bin/env python3

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

class TradingApp(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self, self)
    

app = TradingApp()
