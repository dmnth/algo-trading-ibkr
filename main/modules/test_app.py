#! /usr/bin/env python3

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import Order
from ibapi.contract import Contract
from threading import Timer

#TODO: where contract.description gets assigned at 
# and why is it present in docks but Contract class
# has no attribute with this name.


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

    # END ORDERS

    def start(self):

        contract = Contract()
        contract.symbol = 'VRM'
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.primaryExchange = 'NASDAQ'

        order = Order()
        order.action = 'BUY'
        order.totalQuantity = 200
        order.orderType = 'LMT'
        order.lmtPrice = 1.11
        order.eTradeOnly = False
        order.firmQuoteOnly = False

        #self.reqContractDetails(1, contract)
        #self.reqMatchingSymbols(12, 'VRM')

        print(self.isConnected())
        # try to make an order here:
        order = self.create_auction_order('BUY', 1, 1381)
        contract = self.create_stock_contract('LSE', '41015940')
        self.place_auction_order(contract, order)

        order = self.create_auction_order('BUY', 2, 1382)
        contract = self.create_stock_contract('LSE', '41015940')
        self.place_auction_order(contract, order)

        order = self.create_auction_order('BUY', 2, 1382)
        contract = self.create_stock_contract('LSE', '41015940')
        self.place_auction_order(contract, order)
        #self.placeOrder(self.nextValidOrderId, contract, order)
        # FUTURES
      #  self.get_futures_local_symbol('BN', 'FUT', 'EUR', 'EUREX', 'BSNH DEC 23')
      #  self.get_futures_details_multiplier('BN', 'FUT', 'EUR', 'EUREX', '100')
        #self.get_futures_details_multiplier_x_local_symbol('ZS', 'FUT', 'USD', 'ECBOT', 'ZS NOV 22', '5000')
      #  self.get_futures_details_last_day('BN', 'FUT', 'EUR', 'EUREX', '202312')

        # OPTIONS

      #  self.get_options_details_multiplier('LHA', 'OPT', 'EUR', 'FTA', '140')
      #  self.get_options_details_multiplier_x_lastTrade('LHA', 'OPT', 'EUR', 'FTA', '140', '202306')
    #    self.get_options_details_multiplier_x_lastTrade_x_localSymbol('LHA', 'OPT', 'EUR', 'FTA', '140', '202306', 'LUQ C@4.28 JUN23')
    #    self.get_options_details_multiplier_strike_expirationDate('LHA', 'OPT', 'EUR', 'FTA', '140', '4.28', '202306')
    #   self.get_options_details_multiplier_strike_expirationDate_x_localSymbol('LHA', 'OPT', 'EUR', 'FTA', '140', '4.28', '202306', 'LUQ C@4.28 JUN23')
    #  self.get_options_details_multiplier_strike_expirationDate_x_tradingClass('LHA', 'OPT', 'EUR', 'FTA', '140', '4.28', '202306', 'LUQ')

   # FUTURES OPTIONS

        #self.get_futuresOptions('AZN', 'FOP', 'GBP', 'ICEEU')
        #self.get_futuresOptions_lastTrade_x_strike_x_Right_x_Multiplier('JET', 'OPT', 'GBP', 'ICEEU', '20270219', 15.4, 'C', '1000', 'JEK FEB27 15.4 C', '561577600')
        #self.get_futuresOptions_lastTrade_x_strike_x_Right_x_Multiplier('ET', 'PT', 'BP', 'IU', '20279', 5.4, 'C', '00', 'JEK FEB27 15.4 C', '561577600')
        #self.get_futuresOptions_by_conId('JET', 'OPT', 'GBP', 'ICEEU', '561577600')
        #self.get_futuresOptions_by_localSymbol('JET', 'OPT', 'GBP', 'ICEEU', 'JEK FEB27 15.4 C')
        # self.get_futuresOptions_by_tradingClass('JET', 'OPT', 'GBP', 'ICEEU', 'JEK')
        # self.get_futuresOptions_by_tradingClass_x_right('JET', 'OPT', 'GBP', 'ICEEU', 'JEK', 'C')
        # self.get_futuresOptions_by_tradingClass_x_right_x_strike('JET', 'OPT', 'GBP', 'ICEEU', 'JEK', 'C', 15.4 )
        # self.get_futuresOptions_by_tradingClass_x_right_x_multiplier('JET', 'OPT', 'GBP', 'ICEEU', 'JEK', 'C', '1000' )

    # Should have create a base contract for every single instrument first.

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


