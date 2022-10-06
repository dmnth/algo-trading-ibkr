#! /usr/bin/env python3

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import Order
from ibapi.contract import Contract

class TradingApp(EWrapper, EClient):
    
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    def error(self, reqId: int, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, Msg:' + \
        '{errorString}'
        print(error_message)

app = TradingApp()
