import random
import flask

app = flask.Flask(__name__)

# List of possible colours.
COLOURS = [
    'red', 'orange', 'blue', 'purple',
    '#C0C000',  # dark yellow
    '#00C000'   # dark green
]

# List of possible messages.
MESSAGES = ['Hello, World!', 'Computing is Fun', 'Interesting']

@app.route('/css')
def css():
    border_colour = random.choice(COLOURS)
    text_colour = random.choice(COLOURS)
    return (
        flask.render_template('example.css', 
            border_colour=border_colour,
            text_colour=text_colour),
        { 'Content-Type': 'text/css' }
    )

@app.route('/')
def html():
    msg = random.choice(MESSAGES)
    return flask.render_template('example.html', msg=msg)
        
if __name__ == '__main__':
    app.run()
