from flask_marshmallow import Marshmallow, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

from models import Group, Product

ma = Marshmallow()


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        load_instance = True
        include_relationships = True


