#!/usr/bin/env python
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager

from server.app import app
# For migration
from server.models import *


manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
