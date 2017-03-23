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
CUTLENGTH = 10  # length to shorten hashes

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
    """shorten addresses for readability"""
    print string
    if string:
        return string[0:CUTLENGTH]
    else:
        return ''


@app.template_filter('empl')
def empl(string):
    if string is 'Darren Tseng':
        return 'Thomas Dietert'


@app.template_filter('shorten_key')
def shortkeys(string):
    """shorten keys"""
    if string:
        return string[29:39]
    else:
        return ''


@app.template_filter('peers')
def peers(p):
    """Peers filter"""
    res = matrix.peers()
    results = handle_results(res)
    peers = len(results)

    return peers


@app.template_filter('to_pretty_json')
def to_pretty_json(value):
    return json.dumps(value, sort_keys=True,
                      indent=4, separators=(',', ': '))


@app.template_filter('datetimeformat')
def datetimeformat(unix_timestamp):
    """Filter for converting unix time to human readable"""
    return time.strftime('%m/%d/%Y, %I:%M %p', time.localtime(unix_timestamp))


def handle_results(res):
    """Handles succesful or failed results of server communication"""
    # print "!!!!!!!!!!!!!!!!!!!!"
    # print res
    if res['tag'] == ERROR:
        results = json.load(res)
        print results.contents.errorType
        print results.contents.errorMsg
        error = '{} : {}'.format(
            results.contents.errorType, results.contents.errorMsg)
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

    return render_template('index.html', blockset=blockset)


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
    # print res
    accounts = handle_results(res)

    return render_template('accounts.html', accounts=accounts)


@app.route('/accounts/address', methods=['GET', 'POST'])
def account_by_address():
    """present specific account metadata, lookup by address"""
    address = request.form['submit']
    res = matrix.getaccount(address)
    print res
    accinfo = handle_results(res)

    res = matrix.accounts()
    accounts = handle_results(res)

    return render_template('accounts.html', accounts=accounts, accinfo=accinfo)


@app.route('/assets', methods=['GET', 'POST'])
def show_assets():
    """Present a table of assets"""
    res = matrix.assets()
    assets = handle_results(res)

    return render_template('assets.html', assets=assets)


@app.route('/contracts', methods=['GET', 'POST'])
def show_contracts():
    """Present a table of contracts"""
    res = matrix.contracts()
    contracts = handle_results(res)

    return render_template('contracts.html', contracts=contracts)
