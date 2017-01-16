from flask import Flask
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


@app.route("/")
def output():
    return "Output results here."


if __name__ == "__main__":
    app.run(debug=True)
