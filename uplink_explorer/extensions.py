# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in uplink_explorer.py."""
import os
from uplink.session import UplinkSession
from config import config, ProdConfig

rpc_addr = config.RPC_HOST

print("RPC listening on " + rpc_addr)

# register extensions
uplink = UplinkSession(addr=rpc_addr)

if config == ProdConfig:
    from raven.contrib.flask import Sentry

    # XXX -- remove from open sourcing and put as env var
    sentry = Sentry(dsn='https://8590448340a54eb2a9c47b3628860560:23f589dd7412424ebee127f2a0114dd7@sentry.io/205685')
