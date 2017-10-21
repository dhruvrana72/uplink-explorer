# -*- coding: utf-8 -*-
"""Application configuration."""

import os


class Config(object):
    """Base configuration."""
    READONLY_MODE = not (os.environ.get('READONLY') == "TRUE")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    RPC_HOST = os.environ.get('RPC_HOST', 'localhost')

class ProdConfig(Config):
    """Production configuration."""
    READONLY_MODE = True  # hardcode until we add this to the envs for test net
    DEBUG = False
    SECRET_KEY = 'aaljngtfshafhffgdfg32897tb8c94m3w390sand'


class DevConfig(Config):
    """Development configuration."""
    DEBUG = True
    SECRET_KEY = 'asndaion(#*IWOJsd9adKAvls0aosind'


_config = {
    "DEV": "uplink_explorer.config.DevConfig",
    "PROD": "uplink_explorer.config.ProdConfig",
}


config_path = _config.get(os.environ.get('ENV', "PROD"), _config['PROD'])

config = DevConfig if os.environ.get('ENV') == 'DEV' else ProdConfig
print(config.READONLY_MODE)
