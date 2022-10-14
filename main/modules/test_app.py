#! /usr/bin/env python3

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import Order
from ibapi.contract import Contract
from threading import Timer

#TODO: where contract.description gets assigned at 
# and why is it present in docks but Contract class
# has no attribute with this name.

class TestApp(EWrapper, EClient):
    
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    def error(self, reqId: int, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, '\
                + f'Msg: {errorString}'
        print(error_message)

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        self.start()

    def contractDetails(self, reqId, contractDetails):
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""
        super().contractDetails(reqId, contractDetails)
        print(f"reqID: {reqId}, contract: {contractDetails}")

    def symbolSamples(self, reqId, contractDescriptions):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol samples. Request ID: ", reqId)
        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += " "
                derivSecTypes += derivSecType
            print(f"Contract: {contractDescription.contract.conId}" +\
                    f"Symbol: {contractDescription.contract.symbol}")


    def start(self):
        contract = Contract()
        contract.symbol = 'FUN'
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.primaryExchange = 'NASDAQ'

        order = Order()
        order.action = 'BUY'
        order.totalQuantity = 200
        order.orderType = 'LMT'
        order.lmtPrice = 1.11 

        self.reqContractDetails(1, contract)
        self.reqMatchingSymbols(12, 'VRM')

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('192.168.1.127', 7497, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime()}')
        Timer(3, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()

