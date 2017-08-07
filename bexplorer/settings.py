# -*- coding: utf-8 -*-
"""Application configuration."""

import os


class Config(object):
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    HOST = 'bootnode'
    SECRET_KEY = 'aaljngtfshafhffgdfg32897tb8c94m3w390sand'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    HOST = '0.0.0.0'
    SECRET_KEY = 'asndaion(#*IWOJsd9adKAvls0aosind'


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
