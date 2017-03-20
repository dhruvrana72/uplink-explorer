# -*- coding: utf-8 -*-

import json
import warnings
import time
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError

#from .utils import hex_to_dec, validate_block
from bexplorer.matrix.exceptions import (RpcConnectionFail, BadStatusCodeError, BadJsonError,
                                         BadResponseError)

MATRIX_PORT = 8545


class MatrixJsonRpc(object):

    def __init__(self, host='localhost', port=MATRIX_PORT, tls=False):
        self.host = host
        self.port = port
        self.tls = tls
        self.block = None

    def _call(self, method, params=None, _id=1):
        logging.info("RPC call")

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
        url = '{}://{}:{}'.format(scheme, self.host, self.port)
        #print(url, data)

        try:
            req = requests.post(url, data=json.dumps(data))
        except RequestsConnectionError:
            raise RpcConnectionFail
        if req.status_code / 100 != 2:
            raise BadStatusCodeError(req.status_code)
        try:
            response = req.json()
        except ValueError:
            raise BadJsonError(req.text)
        try:
            return response['result']
        except KeyError:
            raise BadResponseError(response)

    def blocks(self, count=1):
        """List of blocks and transactions"""
        return map(self.block, [i for i in range(0, count)])
