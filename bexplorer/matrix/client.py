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

    def _call(self, method, params=None, _id=1, endpoint=None):
        print 'RPC Call'
        # logging.info("RPC call")
        self.endpoint = endpoint
        params = params or []
        data = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': _id,
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
          Get a list of blocks and transactions
        """

        self.blocks = self._call('GET', endpoint='blocks')
        print self.blocks
        return self.blocks
        # return map(self.blocks, [i for i in range(0, count)])
