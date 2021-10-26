import json

from config.helper_model import ModuleHelper, db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates


class UserModel(ModuleHelper):
    """
        When create new user, after make instance, before save, do instance.hashed_password(password)!!!
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    @validates('password')
    def validate_password(self, key, password):
        check = '1 2 3 4 5 6 7 8 9'.split()
        if not any(i in password for i in check):
            raise ValueError("Password there must be at least one number")
        if not len(password) >= 4:
            raise ValueError("Password must be at least four character")
        return password

    def hashed_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, user_password):
        return check_password_hash(self.password, user_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {"id": self.id, "name": self.name}


class TaxModel(ModuleHelper):
    __tablename__ = 'tax'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer)
    cars = db.relationship('CarModel', backref='cars', lazy='dynamic')


class CarModel(ModuleHelper):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    card = db.Column(db.String(250), unique=True)
    tax_id = db.Column(db.Integer, db.ForeignKey('tax.id'))

    def to_json(self):
        tax_name = TaxModel.find_by_id(self.tax_id)
        return {'name': self.name, 'card': self.card, "tax_id": self.tax_id, "tax_name": tax_name.name}


class ParkingModel(db.Model):
    __tablename__ = 'lot'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    in_lot = db.Column(db.DateTime, default=datetime.now())
    out_lot = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return CarModel.find_by_id(self.car_id)

    def to_json(self):
        a = CarModel.find_by_id(self.car_id)
        print()
        return {'name': a.name, 'in': str(self.in_lot)}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
