# -*- coding: utf-8 -*-
"""Streamer"""
import time
import os
import json
import random
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, session, g, redirect, render_template, \
    url_for, abort, flash, jsonify

import codecs
from matrix.session import MatrixSession
from matrix.utils import ecdsa_new
from utils import formatPrec, printer

# set app
app = Flask(__name__)
# matrix = MatrixSession(addr='35.187.112.104')
matrix = MatrixSession()
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

    if value:
        if atype['type'] == 'Discrete':
            return value

        if atype['type'] == 'Fractional':

            prec = atype['precision']
            result = formatPrec(prec, value)
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
        printer(res, "Error")
        results = res
        jsonified = jsonify(res)
        loaded = json.loads(jsonified.data)
        results = loaded['contents']
        error = 'Error: {} : {}'.format(
            results['errorType'], results['errorMsg'])
        flash(error, 'error')

    else:
        printer(res, "Results")
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
    transactions = handle_results(res)

    return render_template('transactions.html', transactions=transactions, block_id=block_id)


@app.route('/transactions/details', methods=['GET', 'POST'])
def show_tx_details():
    """Present a table of transaction details"""

    block_id = request.form['block_id']
    res = matrix.transactions(block_id)
    transactions = handle_results(res)

    res = request.form['submit']
    details = eval(res)

    return render_template('transactions.html', transactions=transactions, block_id=block_id,
                           details=details)


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

    pubkey, skey = ecdsa_new()
    privkey = skey.to_string()
    private_key_hex = codecs.encode(privkey, 'hex')

    matrix.create_account(privkey=private_key_hex)
    res = matrix.accounts()
    accounts = handle_results(res)

    return render_template('accounts.html', accounts=accounts)


@app.route('/accounts/address', methods=['GET', 'POST'])
def account_by_address():
    """present specific account metadata, lookup by address"""
    address = request.form['submit']
    res = matrix.getaccount(address)

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

    name = request.form['name']
    supply = request.form['supply']
    asset_type = request.form['asset_type']
    reference = request.form['reference']

    matrix.create_asset(name, supply, asset_type, reference)

    res = matrix.assets()
    assets = handle_results(res)

    return render_template('assets.html', assets=assets)


@app.route('/assets/holdings', methods=['GET', 'POST'])
def asset_holdings():
    """get holdings of assets"""
    asset_type = request.form['atype']

    #  checks if precision exists
    if request.form['prec'] is not False:
        prec = request.form['prec']
        atype = {u'type': asset_type, u'precision': prec}
    else:
        atype = {u'type': asset_type}

    res = request.form['submit']
    holdings = eval(res)

    res = matrix.assets()
    assets = handle_results(res)

    return render_template('assets.html', assets=assets, holdings=holdings, atype=atype)


@app.route('/contracts', methods=['GET', 'POST'])
def show_contracts():
    """Present a table of contracts"""
    res = matrix.contracts()

    contracts = handle_results(res)
    # print contracts
    return render_template('contracts.html', contracts=contracts)


@app.route('/contracts/create', methods=['GET', 'POST'])
def create_contract():
    """Create new contract"""

    script = request.form['script']
    res = matrix.create_contract(script)
    new_contract_addr = handle_results(res)

    res = matrix.contracts()
    contracts = handle_results(res)

    return render_template('contracts.html', contracts=contracts, new_contract_addr=new_contract_addr)
