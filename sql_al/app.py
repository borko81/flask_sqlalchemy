from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)

# #########################################################POST####################################################################
#  curl http://127.0.0.1:5000/user -X POST -d '{"username": "BOBO1", "email": "bobko1@abv.bg"}' -H "content-type: application/json"
# #################################################################################################################################


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(36), unique=True, nullable=False)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user', lazy=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class ShowAllUsers(Resource):
    def get(self):
        q = User.query.all()
        schema = UserSchema(many=True)
        return schema.dump(q)

    def post(self):
        data = request.get_json()
        # print("-"*100)
        # print(data)
        # print("-" * 100)
        u = User(username=data['username'], email=data['email'])
        db.session.add(u)
        db.session.commit()
        return {"message": 'New User create Successfully'}, 201


class UserShow(Resource):
    def get(self, id):
        q = User.query.filter_by(id=id).first()
        schema = UserSchema()
        return schema.dump(q)


api.add_resource(ShowAllUsers, '/user')
api.add_resource(UserShow, '/user/<id>')

if __name__ == '__main__':
    app.run(debug=True)
