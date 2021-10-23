from config import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def hashed_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, user_password):
        return check_password_hash(self.password, user_password)

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_user_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class TownModel(db.Model):
    __tablename__ = 'town'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    names = db.relationship('NameModel', lazy='dynamic', backref='names')

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_from_name(cls, name):
        return cls.query.filter_by(name=name).first()


class NameModel(db.Model):
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    town_id = db.Column(db.Integer, db.ForeignKey('town.id'))

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()