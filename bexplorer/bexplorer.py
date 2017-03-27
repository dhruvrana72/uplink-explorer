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
FPREC = 0.0000001
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


@app.template_filter('shorten_key')
def shortkeys(string):
    """shorten keys"""
    if string:
        return string[30:40]
    else:
        return ''


@app.template_filter('peers')
def peers(p):
    """Peers filter"""
    res = matrix.peers()
    results = handle_results(res)
    peers = len(results)

    return peers


@app.template_filter('convert')
def convert(value, atype):
    """
        convert asset type fractional to fixed precision
        FPREC is 10^(-7) or 0.0000001
    """
    # print '=================='
    # print value, atype
    # print '=================='

    if value:
        if atype['type'] == 'Discrete':
            return value

        if atype['type'] == 'Fractional':
            # print '======FRAC VAL======='
            # print value
            result = value * FPREC
            return result

        if atype['type'] == 'Binary':
            if value <= 0:
                return 'not held'
            else:
                return 'held'
    else:
        return 'error with asset type'


@app.template_filter('to_pretty_json')
def to_pretty_json(value):
    return json.dumps(value, sort_keys=True,
                      indent=4, separators=(',', ': '))


@app.template_filter('datetimeformat')
def datetimeformat(unix_timestamp):
    # print '--------------'
    # print unix_timestamp
    # print '---------------'
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
        results = loaded['contents']

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
    print '======TX========'
    print res
    print '======TX========'
    transactions = handle_results(res)

    return render_template('transactions.html', transactions=transactions)


@app.route('/accounts', methods=['GET', 'POST'])
def show_accounts():
    """Present a table of accounts"""
    res = matrix.accounts()
    # print res
    accounts = handle_results(res)

    return render_template('accounts.html', accounts=accounts)


@app.route('/accounts/create', methods=['GET', 'POST'])
def create_account():
    """Create an Account"""
    res = matrix.create_account()
    # newacct = handle_results(res)
    print "=====New Account======"
    # print newacct
    print res
    print "=====/New Account/===="

    res = matrix.accounts()
    accounts = handle_results(res)
    return render_template('accounts.html', accounts=accounts)


@app.route('/accounts/address', methods=['GET', 'POST'])
def account_by_address():
    """present specific account metadata, lookup by address"""
    address = request.form['submit']
    res = matrix.getaccount(address)
    # print res
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


@app.route('/assets/create', methods=['GET', 'POST'])
def create_asset():
    """Create a new asset"""
    # print request.form['submit']
    # print request.form
    name = request.form['name']
    supply = request.form['supply']
    asset_type = request.form['asset_type']
    reference = request.form['reference']
    # print '========!!!!!!!!=========='
    # print name
    # print supply
    # print asset_type
    # print reference
    # print '========!!!!!!!!=========='
    matrix.create_asset(name, supply, asset_type, reference)

    res = matrix.assets()
    assets = handle_results(res)

    return render_template('assets.html', assets=assets)


@app.route('/assets/holdings', methods=['GET', 'POST'])
def asset_holdings():
    """get holdings of assets"""
    asset_type = request.form['atype']
    atype = {u'type': asset_type}

    res = request.form['submit']
    holdings = eval(res)

    # print '========!!!!!!!!=========='
    # print holdings
    # print '========!!!!!!!!=========='

    res = matrix.assets()
    assets = handle_results(res)

    return render_template('assets.html', assets=assets, holdings=holdings, atype=atype)


@app.route('/contracts', methods=['GET', 'POST'])
def show_contracts():
    """Present a table of contracts"""
    res = matrix.contracts()

    contracts = handle_results(res)
    print contracts
    return render_template('contracts.html', contracts=contracts)


@app.route('/contracts/create', methods=['GET', 'POST'])
def create_contract():
    """Create new contract"""

    script = request.form['script']
    res = matrix.create_contract(script)
    new_contract_addr = handle_results(res)
    # print '=========script=========='
    # print new_contract_addr
    # print '=========script=========='

    res = matrix.contracts()
    contracts = handle_results(res)

    return render_template('contracts.html', contracts=contracts, new_contract_addr=new_contract_addr)
