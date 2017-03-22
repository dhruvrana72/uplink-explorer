# -*- coding: utf-8 -*-
"""Streamer"""
import time
import os
import json
import random
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, session, g, redirect, render_template, \
    url_for, abort, flash, jsonify
from matrix.session import MatrixSession

# set app
app = Flask(__name__)
matrix = MatrixSession(addr='54.163.224.249')
# matrix = MatrixSession()
matrix.init_app(app)

# env = Environment(loader=FileSystemLoader('/templates'))

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


@app.template_filter('shorten')
def shorten(string):
    print string
    if string:
        return string[0:10]
    else:
        return ''


@app.template_filter('datetimeformat')
def datetimeformat(unix_timestamp):
    """Filter for converting unix time to human readable"""
    return time.strftime('%m/%d/%Y, %I:%M %p', time.localtime(unix_timestamp))


def handle_results(res):
    """Handles succesful or failed results of server communication"""

    if res['tag'] is ERROR:
        results = json.load(res)
        print results._data.errorType
        print results._data.errorMsg
        error = '{} : {}'.format(
            results._data.errorType, results._data.errorMsg)
        flash(error)
        results = error
    else:
        jsonified = jsonify(res)
        loaded = json.loads(jsonified.data)
        results = loaded['_data']

    return results


@app.route('/', methods=['GET', 'POST'])
def show_index():
    """Main Index Page"""

    # BLOCKS
    res = matrix.blocks()
    blockset = handle_results(res)

    # PEERS
    res = matrix.peers()
    results = handle_results(res)
    peers = len(results)

    return render_template('index.html', blockset=blockset, peers=peers)


@app.route('/transactions', methods=['GET', 'POST'])
def show_transactions():
    """Present a table of transactions"""
    block_id = request.form['submit']

    res = matrix.transactions(block_id)
    transactions = handle_results(res)

    return render_template('transactions.html', transactions=transactions)


@app.route('/accounts', methods=['GET', 'POST'])
def show_accounts():
    """Present a table of accounts"""
    res = matrix.accounts()
    accounts = handle_results(res)

    return render_template('accounts.html', accounts=accounts)


@app.route('/assets', methods=['GET', 'POST'])
def show_assets():
    """Present a table of assets"""
    res = matrix.assets()
    assets = handle_results(res)

    return render_template('assets.html', assets=assets)
