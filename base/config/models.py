from config import db


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