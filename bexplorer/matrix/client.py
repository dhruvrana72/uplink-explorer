# -*- coding: utf-8 -*-

import json
import warnings
import time
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError

# from .utils import hex_to_dec, validate_block
from bexplorer.matrix.exceptions import (RpcConnectionFail, BadStatusCodeError, BadJsonError,
                                         BadResponseError)

MATRIX_PORT = 8545


class MatrixJsonRpc(object):
    """
      JSON RPC For Matrix
    """

    def __init__(self, host='localhost', port=MATRIX_PORT, tls=False, endpoint=None):
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.tls = tls
        self.blocks = None
        self.peers = None
        self.account = None
        self.accounts = None
        self.newaccount = None
        self.transactions = None
        self.assets = None
        self.contracts = None

    def _call(self, method, params=None, endpoint=None):
        print 'RPC Call'
        # logging.info("RPC call")
        self.endpoint = endpoint
        params = params or []
        data = {
            'method': method,
            'params': params,
        }
        scheme = 'http'
        if self.tls:
            scheme += 's'
        if self.endpoint is None:
            url = '{}://{}:{}'.format(scheme, self.host, self.port)
        else:
            url = '{}://{}:{}/{}'.format(scheme, self.host,
                                         self.port, self.endpoint)
        print(url, data)

        try:
            req = requests.post(url, data=json.dumps(data))
        except RequestsConnectionError:
            raise RpcConnectionFail
        if req.status_code / 100 != 2:
            raise BadStatusCodeError(req.status_code)
        try:
            response = req.json()
        except ValueError:
            raise BadJsonError(req.error)
        try:
            return response
        except KeyError:
            raise BadResponseError(response)

    def matrix_blocks(self, count=1):
        """
          Get a list of blocks
        """

        self.blocks = self._call('GET', endpoint='blocks')
        return self.blocks

    def matrix_peers(self):
        """
          Get a list of peers and return number of peers
        """
        self.peers = self._call('GET', endpoint='peers')
        return self.peers

    def matrix_transactions(self, block_id=0):
        """
          Get a list of transactions by block index
        """
        self.transactions = self._call('GET', endpoint='transactions')
        return self.transactions

    def matrix_accounts(self):
        """
          Get a list of accounts
        """
        self.accounts = self._call('GET', endpoint='accounts')
        return self.accounts

    def matrix_getaccount(self, address):
        """
          Get individual account by address [/accounts/<address>]
        """
        account_by_address = 'accounts/{}'.format(address)
        self.account = self._call('GET', endpoint=account_by_address)

        return self.account

    def matrix_createaccount(self):
        """
          Create new account
        """
        self.newaccount = self._call('POST', endpoint='account/create')

    def matrix_assets(self):
        """
          Get a list of assets
        """
        self.assets = self._call('GET', endpoint='assets')
        return self.assets

    def matrix_contracts(self):
        """
          Get a list of contacts
        """
        self.contracts = self._call('GET', endpoint='contracts')
        return self.contracts
