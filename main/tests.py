#! /usr/bin/env python3

import pytest
from modules.test_app import TestApp 

from ibapi.order import Order
from ibapi.contract import Contract
from threading import Timer

# TODO: test fixtures, historical data

app = TestApp()

class TestIbgateway:

    @classmethod
    def setup_class():
        print('Connecting...')
        app.connect('192.168.1.167', 7497,
                clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime()}')

    @classmethod
    def teardown_class():
        print('Connection terminated...')
        if app.isConnected() == True:
            app.disconnect()
        print('Connection time: {0}'.format(app.twsConnectionTime()))

    def test_is_connected(self):
        assert app.isConnected() == True 

    def test_can_retrieve_id(self):
        assert app.clientId != None
    
    def test_disconnect(self):
        app.disconnect()
        assert app.isConnected() == False

@pytest.fixture()
def connect():
    app.connect('192.168.1.167', 7497, clientId=0)
    Timer(3, app.stop).start()
    app.run()
    yield 
    app.disconnect()

def test_order_exists(connect):
    assert False



