from flask import Flask, render_template, request, redirect
from flask.ext.migrate import Migrate

from .db import db


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
        return redirect('results')
    return render_template('index.html')


@app.route('/results')
def results():
    return 'Sup'


if __name__ == "__main__":
    app.run(debug=True)
