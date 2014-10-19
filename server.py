import sqlite3
import os
from contextlib import closing
from flask import Flask, g, flash
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

# DATABASE = './links.db'
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    assignment = db.relationship('Assignment', backref=db.backref('links', lazy='dynamic'))

    def __init__(self, link, assignment):
        self.link = link
        self.assignment = assignment

    def __repr__(self):
        return '<Link %r>' % self.link


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String)
    name = db.Column(db.String, unique=True)

    def __init__(self, kind, name):
        self.kind = kind
        self.name = name

    def __repr__(self):
        return '<Assignment %r>' % self.name

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
