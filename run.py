# -*- coding: utf-8 -*-
"""Run bexplorer application. Similar to manage.py"""
from bexplorer.bexplorer import *
from flask_script import Command, Manager, Option, Server

manager = Manager(app)


class Server(Command):
    """Initializes server"""

    def get_options(self):
        return ()

    def run(self):
        print("Running server.")
        server = app.run(host='0.0.0.0', port=5000)

manager.add_command('server', Server())

if __name__ == '__main__':
    manager.run()
