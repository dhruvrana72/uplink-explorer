
# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in bexplorer.py."""
import os
from settings import Config, ProdConfig, DevConfig

from uplink.session import UplinkSession

CONFIG = ProdConfig if os.environ.get('ENV') == 'prod' else DevConfig

rpc_addr = os.getenv('HOST') or CONFIG.HOST

print("RPC listening on " + rpc_addr)

# register extensions
uplink = UplinkSession(addr=rpc_addr)
