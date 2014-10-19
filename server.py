import sqlite3
import os
import json
from contextlib import closing
from flask import Flask, g, flash, jsonify
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

@app.route('/labs/')
def labs():
    results = {}

@app.route('/hws/')
def hws():
    results = {}
    for a in Assignment.query.filter_by(kind='hw').all():
        links = json.dumps([l.link for l in a.links.all()])
        results.update({a.name: links})
    return jsonify(results)

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
