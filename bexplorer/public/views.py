"""
Pages serving HTML content that interact with Flask
"""
import time
import os
import json
import random
import base64
import codecs
from flask import Flask, Blueprint, redirect, render_template, request, url_for, current_app, jsonify, flash

from bexplorer.extensions import uplink
from bexplorer.utils import printer, save_key, read_key

from uplink.cryptography import ecdsa_new, make_qrcode, derive_account_address

blueprint = Blueprint(
    'public', __name__, static_folder='../static', template_folder='../templates')


def handle_results(res):
    """Handles successful or failed results of new contract interactions"""

    if res['errorMsg']:
        jsonified = jsonify(res)
        result = json.loads(jsonified.data)
        error = 'Error: {} : {}'.format(
            result['errorType'], result['errorMsg'])
        flash(error, 'error')
        return
    else:
        return res


@blueprint.route('/', methods=['GET', 'POST'])
def show_index():
    """Main Index Page and blocks"""

    blockset = uplink.blocks()

    return render_template('index.html', blockset=blockset)


@blueprint.route('/transactions', methods=['GET', 'POST'])
def show_transactions():
    """Present a table of transactions"""
    block_id = request.form['submit']
    transactions = uplink.transactions(block_id)

    return render_template('transactions.html', transactions=transactions, block_id=block_id)


@blueprint.route('/transactions/details', methods=['GET', 'POST'])
def show_tx_details():
    """Present a table of transaction details"""

    block_id = request.form['block_id']
    transactions = uplink.transactions(block_id)

    res = request.form['submit']
    details = eval(res)

    return render_template('transactions.html', transactions=transactions, block_id=block_id,
                           details=details)


@blueprint.route('/accounts', methods=['GET', 'POST'])
def show_accounts():
    """Present a table of accounts"""
    accounts = uplink.accounts()
    return render_template('accounts.html', accounts=accounts)


@blueprint.route('/accounts/create', methods=['GET', 'POST'])
def create_account():
    """Create an Account"""

    pubkey, skey = ecdsa_new()
    privkey = skey.to_string()
    uplink.set_key(skey, pubkey)

    uplink.create_account(new_pubkey=pubkey, metadata={})
    public_key_hex = codecs.encode(pubkey.to_string(), 'hex')

    new_acct_pubkey_qr = make_qrcode(
        public_key_hex, "new_acct_pubKey")

    acct_addr = derive_account_address(pubkey)

    new_acct_addr_qr = make_qrcode(acct_addr, "new_acct_address")

    accounts = uplink.accounts()

    # save pem of private key by short address account address as name
    privkey_pem = skey.to_pem()
    name = acct_addr[0:10]
    save_key(privkey_pem, name)

    new_account = None
    while uplink.getaccount(acct_addr) is False:
        time.sleep(3)
        if uplink.getaccount(acct_addr) is not False:
            new_account = uplink.getaccount(acct_addr)

    return render_template('accounts.html', accounts=accounts, newaccount=new_account, new_acct_pubkey_qr=new_acct_pubkey_qr, new_acct_addr_qr=new_acct_addr_qr)


@blueprint.route('/accounts/address', methods=['GET', 'POST'])
def account_by_address():
    """present specific account metadata, lookup by address"""
    address = request.form['submit']
    accinfo = uplink.getaccount(address)

    pubkey = accinfo.public_key
    addr = accinfo.address

    pubkey_qr = make_qrcode(pubkey, "pubKey")
    addr_qr = make_qrcode(addr, "address")

    accounts = uplink.accounts()

    return render_template('accounts.html', accounts=accounts, accinfo=accinfo, pubkey_qr=pubkey_qr, addr_qr=addr_qr)


@blueprint.route('/assets', methods=['GET', 'POST'])
def show_assets():
    """Present a table of assets"""
    assets = uplink.assets()

    return render_template('assets.html', assets=assets)


@blueprint.route('/assets/create', methods=['GET', 'POST'])
def create_asset():
    """Create a new asset"""

    name = request.form['name']
    supply = int(request.form['supply'])
    asset_type = request.form['asset_type']
    reference = request.form['reference']
    issuer = request.form['issuer']
    from_address = issuer

    newasset_addr = uplink.create_asset(
        from_address, name, supply, asset_type, reference, issuer, precision=0)

    assets = uplink.assets()

    newasset_details = None
    while uplink.getasset(newasset_addr) is False:
        time.sleep(3)
        asset_details = uplink.getasset(newasset_addr)
        if asset_details:
            print(newasset_details)

    return render_template('assets.html', assets=assets, new_asset=newasset_details, new_asset_address=newasset_addr)


@blueprint.route('/assets/holdings', methods=['GET', 'POST'])
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
    assets = uplink.assets()

    return render_template('assets.html', assets=assets, holdings=holdings, atype=atype)


@blueprint.route('/contracts', methods=['GET', 'POST'])
def show_contracts():
    """Present a table of contracts"""
    contracts = uplink.contracts()

    script = "global int x = 0; \nlocal int y = 0; \nasset z = '32Gp2CcFx9dagEyZA6UvY7WFiwCp3b8tbTufDYDxdxHj'; \n \nsetX () { \n  x = 42; \n} \n \ngetX () { \n  return x; \n}"

    return render_template('contracts.html', contracts=contracts, script=script)


@blueprint.route('/contracts/create', methods=['GET', 'POST'])
def create_contract():
    """Create new contract"""

    script = request.form['script']
    res = uplink.create_contract(script)
    new_contract_addr = handle_results(res)

    contracts = uplink.contracts()

    return render_template('contracts.html', contracts=contracts, new_contract_addr=new_contract_addr, script=script)


@blueprint.route('/transactions/pending', methods=['GET', 'POST'])
def pending_transactions():
    """Get Pending Transactions from Memory Pool"""
    pending_tx = uplink.get_mempool()

    return render_template('pending_tx.html', pending=pending_tx)
