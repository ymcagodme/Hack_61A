import sqlite3
import os
from contextlib import closing
from flask import Flask, g, flash

# DATABASE = './links.db'
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'links.db'),
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.route('/add/<link>')
def add_links(link):
    db = get_db()
    db.cursor().execute('insert into entries (year, term, type, title, link, checksum) values (?, ?, ?, ?, ?, ?)',
                ["2014", "Fall", "hw", link, link, "123"])
    db.commit()
    return link

@app.route('/')
def hello_world():
    init_db()
    return "Hello World!"

if __name__ == '__main__':
    app.run()
