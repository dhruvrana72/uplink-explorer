# -*- coding: utf-8 -*-
"""Streamer"""
import time
import os
import json
import random
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, session, g, redirect, \
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


def datetimeformat(unix_timestamp):
    '''Filter for converting unix time to human readable'''
    return time.strftime('%m/%d/%Y, %I:%M %p', time.localtime(unix_timestamp))


def render_template(template=None, **kwargs):
    '''
        render template and set environment filters
    '''
    # set root and template directory paths
    ROOT = os.path.abspath(os.path.dirname(__file__))
    TEMPLATES_DIR = os.path.join(ROOT, 'templates')

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    # Adding filters to enviroment to make them visible in the template
    env.filters['datetimeformat'] = datetimeformat

    template_file = env.get_template(template)
    rendered_template = template_file.render(**kwargs)

    return rendered_template


@app.route('/', methods=['GET', 'POST'])
def show_index():
    """
        Main Index Page
    """
    # BLOCKS
    res = matrix.blocks()

    if res['tag'] is ERROR:
        results = json.load(res)
        print results._data.errorType
        print results._data.errorMsg
        # default blockset
        blockset = [{
            'header': {
                'timestamp': 1490101944,
                'origin': '0x123',
                'prevBlock': '0x321',
                'merkleRoot': '0x000'
            },
            'transactions': [],
        }]
    else:
        results = jsonify(res)
        loaded = json.loads(results.data, encoding='utf-8')
        blockset = loaded['_data']

    # PEERS
    res = matrix.peers()

    if res['tag'] is ERROR:
        results = json.load(res)
        print results._data.errorType
        print results._data.errorMsg
        peers = 0
    else:
        results = jsonify(res)
        loaded = json.loads(results.data)
        peers = len(loaded['_data'])

    return render_template('index.html', blockset=blockset, peers=peers)
