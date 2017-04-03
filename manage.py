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


manager.add_command('server', Server())

if __name__ == '__main__':
    manager.run()
