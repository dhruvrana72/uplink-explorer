# -*- coding: utf-8 -*-
"""Run bexplorer application. Similar to manage.py"""
from bexplorer.bexplorer import *
from flask_script import Command, Manager, Option, Server
from gevent import pywsgi

manager = Manager(app)
# DEBUG FALSE BEFORE DEPLOYING!
DEBUG = False
KEYPATH = None
CERTPATH = None


class Server(Command):
    """Initializes server"""

    def __init__(self, secure=False):
        self.secure = secure

    def get_options(self):
        return [
            Option('-s', '--secure', dest='secure',
                   default=self.secure)
        ]

    def run(self):
        secure = secure.lower() == "true"
        if secure:
            print("Running websocket server in secure ssl mode.")
            server = pywsgi.WSGIServer(
                ('', 5001), app, keyfile=KEYPATH, certfile=CERTPATH)
        else:
            print("Running websocket server.")
            server = pywsgi.WSGIServer(('', 5001), app)

        server.serve_forever()

        # print("Running server.")
        # server = app.run(host='0.0.0.0', port=5000, debug=DEBUG)


manager.add_command('server', Server())

if __name__ == '__main__':
    manager.run()
