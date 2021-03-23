import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('stylish.html')

if __name__ == '__main__':
    app.run()

