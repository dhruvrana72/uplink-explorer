# -*- coding: utf-8 -*-
"""Run bexplorer application. Similar to manage.py"""
from bexplorer.bexplorer import *
from flask_script import Command, Manager, Option
# from gevent import pywsgi

manager = Manager(app)
KEYPATH = None
CERTPATH = None


@manager.option('--host', '-h', dest='host')
@manager.option('--port', '-p', dest='port')
def runserver(host="0.0.0.0", port=5000):
    """Run server"""

    print("Running server.")
    app.run(host=host, port=port, debug=False)


class Test(Command):
    """Run test suite"""

    def get_options(self):
        return ()

    def run(self):
        import pytest
        HERE = os.path.abspath(os.path.dirname(__file__))
        TEST_PATH = os.path.join(HERE, 'tests')
        exit_code = pytest.main(
            [TEST_PATH, '--verbose', '--junitxml=$CIRCLE_TEST_REPORTS/summary.xml'])
        return exit_code

manager.add_command('test', Test())

if __name__ == '__main__':
    manager.run()
