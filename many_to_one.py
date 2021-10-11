import json

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'botk@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///many_to_one.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    products = db.relationship('Products', backref='group_owner', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    dr_id = db.Column(db.Integer, db.ForeignKey('group.id'))


if __name__ == '__main__':
    app.run(debug=True)
