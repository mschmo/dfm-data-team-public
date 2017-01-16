from flask import Flask


app = Flask(__name__)


@app.route("/")
def output():
    return "Output results here."


if __name__ == "__main__":
    app.run(debug=True)
