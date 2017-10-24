"""
Pages serving HTML content that interact with Flask
"""

import json
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, BooleanField, DateTimeField, TextField, HiddenField
from wtforms.validators import DataRequired

import gevent
from os import listdir
from os.path import isfile, join
from flask import Blueprint, render_template, request, jsonify, flash
from uplink.cryptography import ecdsa_new, make_qrcode, derive_account_address
from uplink.cryptography import read_key, save_key
from uplink.exceptions import UplinkJsonRpcError, RpcConnectionFail
from uplink_explorer.config import config, ProdConfig
from functools import wraps
from flask import redirect, url_for, flash
from uplink import exceptions

from uplink_explorer.extensions import uplink

# this number should go somewhere better
maxNum = 922337203685.4775807


def readonly_mode_check(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if config.READONLY_MODE:
            flash("Uplink explorer is running in readonly mode")
            return redirect(url_for('public.index'))
        return func(*args, **kwargs)

    return decorated_function


blueprint = Blueprint(
    'public', __name__, static_folder='../static', template_folder='../templates')

example_script = """
global int x = 0 ;

transition initial -> get;
transition get -> terminal;

@get
getX () {
  terminate("Now I die.");
  return x;
}

@initial
setX () {
  x = 42;
  transitionTo(:get);
  return void;
}
"""


@blueprint.context_processor
def inject_version():
    try:
        version = uplink.version()
    except RpcConnectionFail:
        version = dict(commit='UNKNOWN', dirty=False,
                       version='UNKNOWN', branch='UNKNOWN')
    return dict(version=version)


@blueprint.context_processor
def peers():
    try:
        peers = len(uplink.peers())
    except RpcConnectionFail:
        peers = 0
    return dict(peers=peers)


@blueprint.context_processor
def inject_config():
    return dict(config=config)


@blueprint.errorhandler(RpcConnectionFail)
def handle_rpc_connection_fail(error):
    if config == ProdConfig:
        from uplink_explorer.extensions import sentry
        sentry.captureException()

    return render_template("rpc_error.html", title="RPC connection failed", tag='',
                           message="Failed to connect to the RPC server at {}".format(config.RPC_HOST))


@blueprint.errorhandler(UplinkJsonRpcError)
def handle_rpc_error(error):
    title = error.response.get("contents", dict()).get("errorType")
    tag = error.response.get("tag")
    message = error.response['contents']['errorMsg']

    if config == ProdConfig and tag not in ["NotFound"]:
        from uplink_explorer.extensions import sentry
        sentry.captureException()

    return render_template("rpc_error.html", title=title, tag=tag, message=message)


def handle_results(res):
    """Handles successful or failed results of new contract interactions"""

    if res.get("errorMsg"):
        jsonified = jsonify(res)
        result = json.loads(jsonified.data)
        error = 'Error: {} : {}'.format(
            result['errorType'], result['errorMsg'])
        flash(error, 'error')
        return
    else:
        return res


@blueprint.route('/', methods=['GET'])
def blocks():
    """Block list"""
    return render_template('blocks.html', blocks=uplink.blocks())


@blueprint.route('/blocks/<block_id>', methods=['GET'])
def transactions(block_id):
    """Present a table of transactions"""
    transactions = uplink.transactions(block_id)
    return render_template('transactions.html', transactions=transactions, block_id=block_id)


@blueprint.route('/blocks/<block_id>/transactions/<tx_id>', methods=['GET'])
def show_tx_details(block_id, tx_id):
    """Present a table of transaction details"""

    transactions = uplink.transactions(block_id)
    details = list(filter(lambda tx: tx.signature == tx_id, transactions))[0]

    return render_template('transactions.html', transactions=transactions, block_id=block_id,
                           details=details)


@blueprint.route('/accounts/')
@blueprint.route('/accounts/<addr>')
def accounts(addr=None):
    """Present a table of accounts"""
    accounts = uplink.accounts()
    if addr:
        account = uplink.getaccount(addr)
    else:
        account = None
    return render_template('accounts.html', accounts=accounts, account=account)


@blueprint.route('/accounts/create', methods=['GET', 'POST'])
@readonly_mode_check
def create_account():
    """Create an Account"""

    pubkey, skey = ecdsa_new()

    metadata = {}
    acct = uplink.create_account(
        private_key=skey,
        public_key=pubkey,
        from_address=None,
        metadata=metadata,
        timezone="GMT"
    )
    privkey_pem = skey.to_pem()
    location = "./keys/{}".format(acct.address)
    save_key(privkey_pem, location)

    count = 0
    while True:
        count += 1
        gevent.sleep(0.2)

        if (count > 60):
            flash("failed to create account", 'error')
        try:
            acct_detail = uplink.getaccount(acct.address)
            print("new account successfully created " + acct_detail.address)
        except UplinkJsonRpcError:
            continue
        break

    return redirect(url_for('public.accounts', addr=acct.address))


@blueprint.route('/assets/')
@blueprint.route('/assets/<addr>')
def assets(addr=None):
    """Present a table of assets"""
    assets = uplink.assets()
    if addr:
        asset = uplink.getasset(addr)
    else:
        asset = None

    return render_template('assets.html', assets=assets, asset=asset, keyfiles=get_keys())


@blueprint.route('/assets/create', methods=['POST'])
@readonly_mode_check
def create_asset():
    """Create a new asset"""

    name = request.form['name']
    supply = request.form['supply']

    asset_type = request.form['asset_type']
    reference = request.form['reference']
    precision = 0
    issuer = request.form['issuer']

    if (str(asset_type) == "Discrete"):
        if int(supply) > maxNum:
            flash("{} given number cannot be larger than {}".format(
                supply, maxNum), 'error')

    if (str(asset_type) == "Fractional"):
        if int(supply) > maxNum:
            flash("{} given number cannot be larger than {}".format(
                supply, maxNum), 'error')

        precision = int(request.form['precision'])
        supply = int(str(supply) + str('0' * precision))

    if precision > 7:
        flash("number cannot be smaller than 0.0000001", 'error')

    from_address = issuer
    location = "./keys/{}.pem".format(issuer)
    private_key = read_key(location)
    result, newasset_addr = uplink.create_asset(
        private_key, from_address, name, supply, asset_type, reference, issuer, precision)
    try:
        result, newasset_addr = uplink.create_asset(
            private_key, from_address, name, supply, asset_type, reference, issuer, precision)
    except UplinkJsonRpcError as result:
        print(result)
        new_contract_addr = ""
        flash(result.response.get('contents').get('errorMsg'), 'error')

    count = 0
    while True:
        count += 1
        gevent.sleep(0.2)
        if count > 60:
            flash("failed to create account", 'error')
        try:
            asset_details = uplink.getasset(newasset_addr)
            print("new asset successfully created " + asset_details.address)
        except UplinkJsonRpcError:
            continue
        break

    return redirect(url_for('public.assets', addr=newasset_addr))


@blueprint.route('/contracts/')
@blueprint.route('/contracts/<addr>', methods=['GET', 'POST'])
def contracts(addr=None):
    """Present a table of contracts"""
    contracts = uplink.contracts()
    if addr:
        # forms = get_contract_method_forms(addr)
        forms = None
        contract = uplink.getcontract(addr)
    else:
        contract = None
        forms = None

    return render_template('contracts.html', contracts=contracts,
                           script=example_script, contract=contract, keyfiles=get_keys(), forms=forms)


#
# @blueprint.route('/contracts/<addr>/call', methods=['POST'])
# def call_contract(addr):
#     method_name = request.form['method_name'].encode()
#     form = get_method_form(addr, method_name)
#
#     if form.validate_on_submit():
#         # issuer
#         location = "./keys/{}.pem".format(issuer)
#         private_key = read_key(location)
#         uplink.call_contract(private_key=private_key, from_address=issuer,
#                              contract_addr=addr,
#                              method=method_name,
#                              args=[VInt(42)])
#     print(form.errors)
#
#     return redirect(url_for('public.contracts', addr=addr))


@blueprint.route('/contracts/create', methods=['GET', 'POST'])
@readonly_mode_check
def create_contract():
    """Create new contract"""
    script = request.form['script']
    issuer = request.form['issuer']
    new_contract_addr = ""

    try:
        location = "./keys/{}.pem".format(issuer)
        private_key = read_key(location)

        try:
            res, new_contract_addr = uplink.create_contract(
                private_key, str(issuer), str(script))
        except UplinkJsonRpcError as result:

            flash(result.response.get('contents').get('errorMsg'), 'error')

    except IOError:
        flash("Invalid issuer address, no key found. Please try again", "error")

    count = 0
    while True:
        count += 1
        gevent.sleep(0.2)

        if (count > 60):
            flash("failed to create contract", 'error')
        try:
            contract = uplink.getcontract(new_contract_addr)
            print("new contract successfully created " + contract.address)
        except UplinkJsonRpcError:
            continue
        break

    return redirect(url_for('public.contracts', addr=new_contract_addr))


@blueprint.route('/transactions/pending', methods=['GET', 'POST'])
def transactions_pending():
    """Get Pending Transactions from Memory Pool"""
    pending_tx = uplink.get_mempool()

    return render_template('pending_tx.html', pending=pending_tx)


def get_contract_method_forms(addr):
    res = uplink.get_contract_callable(addr)
    forms = {method_name: get_method_form(addr, method_name, args) for method_name, args in
             res.iteritems()}

    return forms


def get_method_form(addr, method_name, args=None):
    args = {"fn_int": [["a", "int"]], "fn_float": [["b", "float"]], "fn_void": [["a", "void"]],
            "fn_msg": [["c", "msg"]], "fn_account": [["a", "account"]],
            "fn_bool": [["x", "bool"], ["b", "float"]],
            "fn_asset": [["a", "asset"]], "fn_contract": [["e", "contract"]],
            "never_called": [["a", "void"]]}[method_name]

    form = type(method_name, (FlaskForm,), {"method_name": HiddenField()})

    for (name, typ) in args:
        if typ == "int":
            setattr(form, name, IntegerField(validators=[DataRequired()]))
        elif typ == "float":
            setattr(form, name, FloatField(validators=[DataRequired()]))
        elif typ in ["account", "asset", "contract", "msg"]:
            setattr(form, name, TextField(validators=[DataRequired()]))
        elif typ == "bool":
            setattr(form, name, BooleanField(validators=[DataRequired()]))

    return form(method_name=method_name)


def get_keys():
    path = "./keys/"
    return [f.replace('.pem', '')
            for f in listdir(path) if isfile(join(path, f)) and not f == ".gitkeep"]
