# -*- coding: utf-8 -*-
import itertools
from .client import MatrixJsonRpc
from functools32 import lru_cache


class MatrixSession(object):
    """
      JSON RPC session instance
    """

    def __init__(self, addr=None, port=None):
        self.addr = addr or '127.0.0.1'
        self.port = port or 8545
        self.conn = None
        self.base = None
        self.app = None

    def init_app(self, app):
        """Connect application instance to matrix session"""

        app.extensions = getattr(app, 'extensions', {})
        self.app = app
        # self.app.logger.info("Initialized Adjoint Matrix rpc")

        if app.config['TESTING'] is False:
            self._connect(app)
        else:
            # otherwise noop connection
            pass

    def _connect(self, app):
        print(self.addr, self.port)
        self.conn = MatrixJsonRpc(self.addr, self.port)
        # cache = [self.block(i) for i in range(0,100)]

    def blocks(self, count=1):
        blockset = self.conn.matrix_blocks(count)
        # print blockset
        return blockset

    def peers(self):
        peers = self.conn.matrix_peers()
        return peers

    def transactions(self, block_id=0):
        transactions = self.conn.matrix_transactions(block_id)
        return transactions

    def accounts(self):
        accounts = self.conn.matrix_accounts()
        return accounts

    def assets(self):
        assets = self.conn.matrix_assets()
        return assets
