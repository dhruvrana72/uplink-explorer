

import os
import sys
import optparse
from bexplorer.bexplorer import *
from flask_script import Command, Manager, Option, Shell
from bexplorer.settings import DevConfig, ProdConfig, TestConfig

KEYPATH = None
CERTPATH = None

#------------------------------------------------------------------------
# Envrionment Variables
#------------------------------------------------------------------------

CONFIG = ProdConfig if os.environ.get('ENV') == 'prod' else DevConfig
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

#------------------------------------------------------------------------
# Application Creation ( MAIN ENTRY POINT )
#------------------------------------------------------------------------

app = create_app(CONFIG)

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access app by default."""
    env = dict(app=app)
    return env

#------------------------------------------------------------------------
# Commands
#------------------------------------------------------------------------


class Server(Command):

    def __init__(self, host='127.0.0.1', port=8000, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    def get_options(self):
        return (
            Option('-n', '--host', dest='host', default=self.host),
            Option('-p', '--port', dest='port', default=self.port),
            Option('-d', '--debug', dest='debug', default=self.debug),
        ) 

    def run(self, host, port, debug):
        app.run(
            debug=debug,
            host=host,
            port=port
        )


class Test(Command):
    """Run the tests."""

    def get_options(self):
        return()

    def run(self):
        import pytest
        app.config['TESTING'] = True
        if os.environ.get('CIRCLE_TEST_REPORTS'):
            print("Running under Circle CI")
            exit_code = pytest.main(
                [TEST_PATH, '--verbose', '--junitxml=$CIRCLE_TEST_REPORTS/summary.xml'])
        else:
            exit_code = pytest.main([TEST_PATH, '--verbose'])
        return exit_code

manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('test', Test())
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()
