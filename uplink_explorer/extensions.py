# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in uplink_explorer.py."""
import os
from uplink.session import UplinkSession
from config import config, ProdConfig
import os
rpc_addr = config.RPC_HOST

print("RPC listening on " + rpc_addr)

# register extensions
uplink = UplinkSession(addr=rpc_addr)

if config == ProdConfig and os.environ.get('SENTRY'):
    from raven.contrib.flask import Sentry

    # XXX -- remove from open sourcing and put as env var
    sentry = Sentry(dsn=os.environ['SENTRY'])
