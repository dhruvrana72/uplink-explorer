# -*- coding: utf-8 -*-
"""Streamer"""
import time
import os
import json
import random

# from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from matrix.session import MatrixSession

# set app
app = Flask(__name__)
matrix = MatrixSession()
matrix.init_app(app)

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
    return render_template('index.html')
