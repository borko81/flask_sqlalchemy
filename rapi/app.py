from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

from models import Product, Group, db
from shemas import ma, ProductSchema, GroupSchema

app = Flask(__name__)
db.init_app(app)
ma.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Product': Product, 'Group': Group}


class ItemResourse(Resource):
    def get(self):
        item_data = Product.query.all()
        schema = ProductSchema(many=True)
        return jsonify(schema.dump(item_data))


class GroupResourse(Resource):
    def get(self):
        group_get = Group.query.all()
        schema = GroupSchema(many=True)
        return jsonify(schema.dump(group_get))


api.add_resource(ItemResourse, '/items')
api.add_resource(GroupResourse, '/groups')


if __name__ == '__main__':
    app.run(debug=True)
