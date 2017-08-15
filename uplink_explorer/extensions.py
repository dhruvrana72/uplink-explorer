# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in uplink_explorer.py."""
import os
from uplink.session import UplinkSession
from config import config

rpc_addr = config.RPC_HOST

print("RPC listening on " + rpc_addr)

# register extensions
uplink = UplinkSession(addr=rpc_addr)
