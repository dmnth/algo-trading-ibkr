#! /usr/bin/env python3

from modules import establish_connection

# TODO: test fixtures, historical data

class TestConnection:

    @classmethod
    def setup_class():
        print('setting up TestConnection class')
        establish_connection.app.connect('192.168.0.211', 4002, clientId=1)

    @classmethod
    def teardown_class():
        print('Tear down TestConnection class')
        establish_connection.app.disconnect()

    def setup_method(self, method):
        print('Establishing connection')
        establish_connection.app.connect('192.168.0.211', 4002, clientId=1)

    def teardown_method(self, method):
        print('Closing connection...')
        establish_connection.app.disconnect()

    def test_can_connect(self):
        print('Time: ',establish_connection.app.reqCurrentTime())
        assert False

