# -*- coding: utf-8 -*-
"""Run bexplorer application. Similar to manage.py"""
from bexplorer.bexplorer import *
from flask_script import Command, Manager, Option, Server
# from gevent import pywsgi

manager = Manager(app)
KEYPATH = None
CERTPATH = None

@manager.command
def runServer(port=5000, debug=False):
    # secure = secure.lower() == "true"
    # if secure:
    #     print("Running websocket server in secure ssl mode.")
    #     server = pywsgi.WSGIServer(
    #         ('', 5001), app, keyfile=KEYPATH, certfile=CERTPATH)
    # else:
    #     print("Running websocket server.")
    #     server = pywsgi.WSGIServer(('', 5001), app)

    # server.serve_forever()
    
    print("Running server.")
    app.run(host="0.0.0.0", port=port, debug=debug)

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
