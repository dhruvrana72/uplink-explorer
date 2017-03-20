# -*- coding: utf-8 -*-
import itertools
from .client import MatrixJsonRpc

# from flask import current_app

from functools32 import lru_cache

# Logging system


class MatrixSession(object):

    def __init__(self, addr=None, port=None):
        self.addr = addr or '127.0.0.1'
        self.port = port or 8545
        self.conn = None
        self.base = None
        self.app = None

    def init_app(self, app):
        app.extensions = getattr(app, 'extensions', {})
        self.app = app
        self.app.logger.info("Initialized Adjoint Matrix rpc")

        if app.config['TESTING'] is False:
            self._connect(app)
        else:
            # otherwise noop connection
            pass

    def _connect(self, app):
        print(self.addr, self.port)
        self.conn = MatrixJsonRpc(self.addr, self.port)
        # self.base = self.conn.matrix_coinbase()
        # cache = [self.block(i) for i in range(0,100)]
