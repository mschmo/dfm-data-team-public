#!/usr/bin/env python
import csv
import gzip
import os

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager

from server.app import app
# For migration
from server.models import *


manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def load_report():
    pass
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with gzip.open(os.path.join(dir_path,  'example_report.csv.gz')) as f:
    #     reader = csv.reader(f)



if __name__ == '__main__':
    manager.run()
