#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import floatToStr


# eTradeOnly and firmQuoteOnly are no longer supported, so are set to False
class baseOrder(Order):

    def __init__(self):
        Order.__init__((self))
        self.eTradeOnly = False
        self.firmQuoteOnly = False


class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def contractDetails(self, reqId, contractDetails):
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""
        super().contractDetails(reqId, contractDetails)
        print(f"reqID: {reqId}, contract: {contractDetails}")

    def bondContractDetails(self, reqId:int, contractDetails):
        super(TestApp, self).bondContractDetails(reqId, contractDetails)
        print(f"reqID: {reqId}, contract: {contractDetails}")
    
    def symbolSamples(self, reqId, contractDescriptions):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol samples. Request ID: ", reqId)
        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += " "
                derivSecTypes += derivSecType
            print(f"Contract: {contractDescription.contract.conId}" + \
                  f"Symbol: {contractDescription.contract.symbol}")

    def tickPrice(self, reqId, tickType, price:float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickeId: ", reqId, "tickType: ", tickType,
              "Price: ", str(price), "CanAoutoExecute: ",
              attrib.canAutoExecute, "PastLimit: ", attrib.pastLimit,
              end=" ")

    def mktDepthExchanges(self, depthMktDataDescriptions):
        super().mktDepthExchanges(depthMktDataDescriptions)
        print("Market Depth Exchanges available: ")
        for desc in depthMktDataDescriptions:
            print(desc)

    def updateMktDepth(self, reqId , position:int, operation:int,
                        side:int, price:float, size:int):
        super().updateMktDepth(reqId, position, operation, side, price, size)
        print("Update Market Depth\n ReqId: ", reqId, "Position: ", position, 'Operation: ',
              operation, "Side: ", side, "Price: ", price, "Size: ", size)

    def updateMktDepthL2(self, reqId, position:int, marketMaker:str,
                          operation:int, side:int, price:float, size:int, isSmartDepth:bool):
        super().updateMktDepthL2(reqId,position, marketMaker, operation, side, price, size, isSmartDepth)
        print("Update Market Depth L2. ReqID: ", reqId, "Position: ", position, "MarketMarker: ", marketMaker,
              "Operation: ", operation, "Side: ", side, "Price: ", price, "Size: ", size,
              "isSmartDepth: ", isSmartDepth)

    def historicalData(self, reqId: int, bar):
        print("Historical data: ", reqId, "BarData: ", bar)

    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: int, askSize: int, tickAttribBidAsk ):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize, askSize, tickAttribBidAsk)
        print('BidAsk. ReqId :', reqId,
              "Time: ", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"),
              "BidPrice: ", floatToStr(bidPrice),
              "AskPrice: ", floatToStr(askPrice),
              "BidSize: ", bidSize,
              "AskSize: ", askSize, "BidPastFlow: ", tickAttribBidAsk.bidPastLow,
              "AskPastHigh: ", tickAttribBidAsk.askPastHigh
            )

    def historicalTicksBidAsk(self, reqId: int, ticks, done: bool):
        super().historicalTicksBidAsk(reqId, ticks, done)
        print("Historical Bid ask. ReqId: ", reqId,
             "ticks: ", ticks, "done: ", done )

    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast , exchange: str,
                          specialConditions: str):
        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAttribLast, exchange,
                                  specialConditions)
        if tickType == 1:
            print("Last.", end="")
        else:
            print("AllLast.", end="")
            print("ReqId: ", reqId,
                  "time: ", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"),
                  "price: ", price, "size", size, "exchange: ", exchange,
                  "Spec COnd: ", specialConditions, "PastLimit: ", tickAttribLast.pastLimit,
                  "Unreported: ", tickAttribLast.unreported)
# END WRAPPERS

    def connectionClosed(self):
        # This function is called upon socket error or connection loss 
        # between TWS and client script.
        print("Connection closed because of reasons")

    def create_base_contact(self, symbol, sectype, currency, exchange):

        contract = Contract()
        contract.symbol = symbol
        contract.secType = sectype
        contract.currency = currency
        contract.exchange = exchange

        return contract

    # FUTURES

    def get_futures_details_multiplier(self, symbol, sectype, currency, exchange, multiplier):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        self.reqContractDetails(661, base_contract)

    def get_futures_details_last_day(self, symbol, sectype, currency, exchange, lastDayTrade):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.lastTradeDateOrContractMonth = lastDayTrade
        self.reqContractDetails(662, base_contract)

    def get_futures_local_symbol(self, symbol, sectype, currency, exchange, local_symbol):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.localSymbol = local_symbol
        self.reqContractDetails(663, base_contract)

    def get_futures_details_multiplier_x_local_symbol(self, symbol, sectype, currency, exchange, local_symbol, multiplier):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        base_contract.localSymbol = local_symbol
        self.reqContractDetails(664, base_contract)

    # OPTIONS

    def get_options_details_multiplier(self, symbol, sectype, currency, exchange, multiplier):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        self.reqContractDetails(665, base_contract)

    def get_options_details_multiplier_x_lastTrade(self, symbol, sectype, currency, exchange, multiplier, lastTrade):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        base_contract.lastTradeDateOrContractMonth = lastTrade
        self.reqContractDetails(666, base_contract)

    def get_options_details_multiplier_x_lastTrade_x_localSymbol(self, symbol, sectype, currency, exchange, multiplier, lastTrade, localSymbol):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        base_contract.lastTradeDateOrContractMonth = lastTrade
        base_contract.localSymbol = localSymbol
        self.reqContractDetails(667, base_contract)


    def get_options_details_multiplier_strike_expirationDate(self,symbol, sectype, currency, exchange, multiplier, strike, expDate):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        base_contract.strike = strike
        base_contract.lastTradeDateOrContractMonth =expDate
        self.reqContractDetails(669, base_contract)

    def get_options_details_multiplier_strike_expirationDate_x_localSymbol(self,symbol, sectype, currency, exchange, multiplier, strike, expDate, localSymbol):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        base_contract.strike = strike
        base_contract.lastTradeDateOrContractMonth =expDate
        base_contract.localSymbol = localSymbol
        self.reqContractDetails(670, base_contract)

    def get_options_details_multiplier_strike_expirationDate_x_tradingClass(self,symbol, sectype, currency, exchange, multiplier, strike, expDate, tradingClass, conId):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        base_contract.strike = strike
        base_contract.lastTradeDateOrContractMonth =expDate
        base_contract.tradingClass = tradingClass
        self.reqContractDetails(671, base_contract)

    # END OPTIONS

    # FUTURES OPTIONS

    def get_futuresOptions(self, symbol, sectype, currency, exchange):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        self.reqContractDetails(761, base_contract)

    def get_futuresOptions_lastTrade_x_strike_x_Right_x_Multiplier(self, symbol, sectype, currency, exchange, lastTrade, strike, right, multiplier, localSymbol, conId):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.multiplier = multiplier
        base_contract.strike = strike
        base_contract.right = right
        base_contract.lastTradeDateOrContractMonth = lastTrade
        base_contract.localSymbol = localSymbol
        base_contract.conId = conId
        self.reqContractDetails(762, base_contract)

    def get_futuresOptions_by_conId(self, symbol, sectype, currency, exchange, conId):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.conId = conId
        self.reqContractDetails(764, base_contract)

    def get_futuresOptions_by_localSymbol(self, symbol, sectype, currency, exchange, localSymbol):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.localSymbol = localSymbol
        self.reqContractDetails(767, base_contract)

    def get_futuresOptions_by_tradingClass(self, symbol, sectype, currency, exchange, tradingClass):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.tradingClass = tradingClass
        self.reqContractDetails(769, base_contract)

    def get_futuresOptions_by_tradingClass_x_right(self, symbol, sectype, currency, exchange, tradingClass, right):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.tradingClass = tradingClass
        base_contract.right = right
        self.reqContractDetails(769, base_contract)

    def get_futuresOptions_by_tradingClass_x_right_x_strike(self, symbol, sectype, currency, exchange, tradingClass, right, strike):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.tradingClass = tradingClass
        base_contract.right = right
        base_contract.strike = strike
        self.reqContractDetails(769, base_contract)

    def get_futuresOptions_by_tradingClass_x_right_x_multiplier(self, symbol, sectype, currency, exchange, tradingClass, right, multiplier):
        base_contract = self.create_base_contact(symbol, sectype, currency, exchange)
        base_contract.tradingClass = tradingClass
        base_contract.right = right
        base_contract.multiplier = multiplier
        self.reqContractDetails(770, base_contract)
    # END FUTURES OPTIONS

    # ORDERS

    def create_limit_order(self, action, quantity, price):
        order = Order()
        order.orderType = 'LMT'
        order.action = action
        order.cashQty = quantity
        order.lmtPrice = price

    def create_auction_order(self, action, quantity, price):
        order = baseOrder()
        order.tif = "AUC"
        order.orderType = "MTL"
        order.action = action
        order.totalQuantity = quantity
        order.lmtPrice = price

        return order

    def create_futures_contract(self, symbol, exchange, currency, localSymbol, mult, lastTrade):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'FUT'
        contract.exchange = exchange
        contract.currency = currency
        contract.localSymbol = localSymbol
        contract.multiplier = mult
        contract.lastTradeDateOrContractMonth = lastTrade

        self.reqContractDetails(3345, contract)

        return contract

    def create_futures_contract_conID(self, exchange, conID):
        contract = Contract()
        contract.exchange = exchange
        contract.conId = conID

        self.reqContractDetails(111111, contract)

        return contract

    def create_stock_contract(self, exchange, conId):
        contract = Contract()
        contract.secType = 'STK'
        contract.exchange = exchange
        contract.conId = conId

        return contract

    def place_auction_order(self, contract, order):
        if contract.exchange not in ['BVME', 'IBIS', 'LSE', 'VSE', 'HKFE', 'TSE']:
            print('Valid exchanges are BVME, IBIS, LSE, VSE, HKFE', 'TSE')
            return
        self.placeOrder(self.nextValidOrderId, contract, order)

    def requestMarketData(self, reqID, contract, genericTickList, snapshot, regulatorySnapShot
                          , mktDataOptions):
        self.reqMktData(reqID, contract, genericTickList, snapshot, regulatorySnapShot, mktDataOptions)

    def request_market_dpth_FX(self, currency1, currency2):
        contract = self.create_base_contact(currency1, 'CASH', currency2, 'IDEALPRO')
        self.reqMktDepth(self.nextValidOrderId, contract, 5, False, [])

    def request_historical_2Y_2018_dayli(self):
        contract = self.create_base_contact('EUR', 'CASH', 'USD', 'IDEALPRO')
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
        queryTime = "20191231-23:59:59"
        self.reqHistoricalData(self.nextValidOrderId, contract, queryTime, "2 Y", "1 day", "MIDPOINT", 1, 1, False, [])

    def request_historical_20Y_200_daily(self):
        contract = self.create_base_contact('EUR', 'CASH', 'USD', 'IDEALPRO')
        self.reqHistoricalData(self.nextValidOrderId, contract, "", "2 Y", "1 day", "BID_ASK", 1, 1, False, [])

    def request_contract_details_ISIN(self):
        contract = Contract()
        contract.symbol = "AMZN"
        contract.secIdType = "ISIN"
        contract.secId = "US0231351067"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        self.reqContractDetails(self.nextValidOrderId, contract)
        self.reqHistoricalData(self.nextValidOrderId, contract, "20221231-23:59:59", "1 Y",
                               "1 day", "BID_ASK", 1, 1, False, [] )


    def start(self):
        print(self.serverVersion())
        contract = Contract()
        contract.symbol = "AMZN"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.secIdType = "ISIN"
        contract.secId = "US0231351067"

        contract = Contract()
        contract.symbol = "EUR"
        contract.exchange = "IDEALPRO"
        contract.secType = "CASH"
        contract.currency = "USD"
        self.reqTickByTickData(self.nextValidOrderId, contract, "AllLast", 0, True)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7497, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()

