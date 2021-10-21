from flask_sqlalchemy import SQLAlchemy
from helper_model import Helper

from config import db


class Group(Helper):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    products = db.relationship('Product', lazy="dynamic")


class Product(Helper):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
