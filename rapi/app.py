from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api, reqparse

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
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help="initialize name")
    parser.add_argument('price', type=float, help="initialize prise")
    parser.add_argument('group_id', type=int, help="initialize group")

    parser.add_argument('new_name', type=str, help="initialize name")
    parser.add_argument('new_price', type=float, help="initialize prise")
    parser.add_argument('new_group_id', type=int, help="initialize group")

    def find_by_name(self, name):
        return Product.find_by_name(name).first()

    def get(self):
        item_data = Product.query.all()
        schema = ProductSchema(many=True)
        return jsonify(schema.dump(item_data))

    def post(self):
        data = ItemResourse.parser.parse_args()
        if self.find_by_name(data['name']):
            return {'message': 'This name not allowed'}, 404
        Product(name=data['name'], price=data['price'], group_id=data['group_id']).save()
        return {"message": "New item was added successfully"}, 201

    def delete(self):
        data = ItemResourse.parser.parse_args()
        product = self.find_by_name(data['name'])
        if not product:
            return {'message': 'Not found product with this name'}, 404
        product.delete()
        return {'message': "Deleted was successfully"}, 204

    def put(self):
        data = ItemResourse.parser.parse_args()
        product = self.find_by_name(data['name'])
        if not product:
            return {'message': 'Not found product with this name'}, 404
        new_name = data['new_name'] or product.name
        new_price = data['new_price'] or product.price
        new_group_id = data['new_group_id'] or product.group_id
        product.name = new_name
        product.price = new_price
        product.group_id = new_group_id
        product.save()
        return {'message': 'Changes was successfully'}, 200


class GroupResourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help="initialize name")
    parser.add_argument('new_name', type=str, help="Used in put method")

    def find_by_name(self, name):
        return Group.find_by_name(name).first()

    def get(self):
        group_get = Group.query.all()
        schema = GroupSchema(many=True)
        return jsonify(schema.dump(group_get))

    def post(self):
        data = GroupResourse.parser.parse_args()
        name = data['name']
        if self.find_by_name(name):
            return {'message': 'This name already exists, try another'}

        g = Group(name=name)
        g.save()
        return {'message': 'Successfully added new item with name {}'.format(name)}, 201

    def delete(self):
        data = GroupResourse.parser.parse_args()
        name = data['name']
        g = self.find_by_name(name)
        if not g:
            return {'message': 'Not found anything to delete with this name'}, 404
        g.delete()
        return {'message': 'Delete was successfully'}, 204

    def put(self):
        data = GroupResourse.parser.parse_args()
        name = data['name']
        new_name = data['new_name']
        g = self.find_by_name(name)
        if not g:
            return {'message': 'Not found anything with this name'}, 404
        g.name = new_name
        return {'message': 'Change was successfully'}, 200


api.add_resource(ItemResourse, '/items')
api.add_resource(GroupResourse, '/groups')

if __name__ == '__main__':
    app.run(debug=True)
