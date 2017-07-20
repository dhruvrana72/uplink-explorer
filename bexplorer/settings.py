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
    HOST = '35.187.112.104'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    HOST = '0.0.0.0'


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
