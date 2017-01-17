import os

from flask import Flask, render_template, request, redirect
from flask.ext.migrate import Migrate

from .db import db
from .models import CampaignFacts


app = Flask(__name__)
# App configurations, override defaults with config_local.py
app.config.from_pyfile('config_default.py')
app.config.from_pyfile('config_local.py', silent=True)
# Initialize SQLalchemy DB object on our app
db.init_app(app)
# Initialize alembic migration object for database migrations
Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        example_file = os.path.join(parent_path,  'example_report.csv.gz')
        out_file = os.path.join(parent_path, 'output_example.csv.gz')
        CampaignFacts.load_from_gzip_csv(example_file, out_file)
        return redirect('results')
    return render_template('index.html')


@app.route('/results')
def results():
    return 'Sup'

