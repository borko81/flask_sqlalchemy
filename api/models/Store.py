from app import db
from typing import List


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    items = db.relationship('ItemModel', lazy="dynamic", primaryjoin="StoreModel.id == ItemModel.store_id")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def json(self):
        return {"name": self.namemz}

    @classmethod
    def find_by_name(cls, name) -> "StoreModel":
        return cls.query.filter_by(name=name)

    @classmethod
    def find_by_id(cls, _id) -> "StoreModel":
        return cls.query.filter_by(id=_id)

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()

