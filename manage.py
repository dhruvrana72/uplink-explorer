# -*- coding: utf-8 -*-
"""Run bexplorer application. Similar to manage.py"""
from bexplorer.bexplorer import *
from flask_script import Command, Manager, Option, Server
# from gevent import pywsgi

manager = Manager(app)
# DEBUG FALSE BEFORE DEPLOYING!
DEBUG = True
KEYPATH = None
CERTPATH = None
PORT = 5000


class Server(Command):
    """Initializes server"""

    # def __init__(self, secure=False):
    # self.secure = secure

    # def get_options(self):
    #     return [
    #         Option('-s', '--secure', dest='secure',
    #                default=self.secure)
    #     ]

    def run(self):
        print("Running server.")
        server = app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
        # secure = secure.lower() == "true"
        # if secure:
        #     print("Running websocket server in secure ssl mode.")
        #     server = pywsgi.WSGIServer(
        #         ('', 5001), app, keyfile=KEYPATH, certfile=CERTPATH)
        # else:
        #     print("Running websocket server.")
        #     server = pywsgi.WSGIServer(('', 5001), app)

        # server.serve_forever()

class Test(Command):
    """Run test suite"""

    def get_options(self):
        return ()

    def run(self):
        import pytest
        HERE = os.path.abspath(os.path.dirname(__file__))
        TEST_PATH = os.path.join(HERE, 'tests')
        exit_code = pytest.main([TEST_PATH, '--verbose', '--junitxml=$CIRCLE_TEST_REPORTS/summary.xml'])
        return exit_code

manager.add_command('server', Server())
manager.add_command('test', Test())

if __name__ == '__main__':
    manager.run()
