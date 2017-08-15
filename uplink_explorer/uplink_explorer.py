# -*- coding: utf-8 -*-
"""Streamer"""

from flask import Flask
from .extensions import uplink
from .public import filters, views


def create_app(config_object):
    """An application factory, as explained here: 
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_blueprints(app)
    uplink.init_app(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(filters.blueprint)
    app.register_blueprint(views.blueprint)

    return None
