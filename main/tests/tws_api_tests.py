#! /usr/bin/env python3

import pytest
from ..modules.test_app import app 

# TODO: test fixtures, historical data
# restrurcture the project, flask as refernce.

class TestTWS:

    @classmethod
    def setup_class():
        print('setting up Test class')
        app.connect('192.168.1.167', 4797,
                clientId=0)

    @classmethod
    def teardown_class():
        print('Tear down Test class')
        if app.isConnected() == True:
            app.disconnect()

    def test_is_connected(self):
        assert app.isConnected() == True 

    def test_can_retrieve_id(self):
        if app.clientId != None:
            assert True
        else:
            assert False
    
    def test_disconnect(self):
        app.disconnect()
        assert app.isConnected() == False
'''
    def setup_method(self, method):
        print('Establishing connection')
        establish_connection.app.connect('192.168.1.167', 4002,
                clientId=2)
    def teardown_method(self, method):
        print('Closing connection...')
        establish_connection.app.disconnect()
'''

