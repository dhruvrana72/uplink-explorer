# -*- coding: utf-8 -*-
"""Streamer"""
import time
import os
import json
import random

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify
from matrix.session import MatrixSession

# set app
app = Flask(__name__)
# matrix = MatrixSession(addr='54.163.224.249')
matrix = MatrixSession()
matrix.init_app(app)

RESPONSE = 'RPCResp'
ERROR = 'RPCRespError'
# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, DATABASE),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('APP_SETTINGS', silent=True)


@app.route('/', methods=['GET', 'POST'])
def show_index():
    """
        Main Index Page
    """

    res = matrix.blocks()

    if res['tag'] is ERROR:
        results = json.load(res)
        print results.data.errorType
        print results.data.errorMsg
        # default blockset
        blockset = [{
            'header': {
                'timestamp': 1490101944,
                'origin': '0x123',
                'prevBlock': '0x321',
                'merkleRoot': '0x000'
            },
            'transactions': {},
        }]
    else:
        results = jsonify(res)
        loaded = json.loads(results.data, encoding='utf-8')
        blockset = loaded['_data']

    return render_template('index.html', blockset=blockset)
