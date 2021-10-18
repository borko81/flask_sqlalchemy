from db import db


class HelpMethod(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()