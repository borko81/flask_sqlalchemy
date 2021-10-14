from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


# #########################################################POST####################################################################
#  curl http://127.0.0.1:5000/user -X POST -d '{"username": "BOBO1", "email": "bobko1@abv.bg"}' -H "content-type: application/json"
# #################################################################################################################################
# curl http://127.0.0.1:5000/user/add_new -X POST -d '{"username": "borko1", "password": "borko", "admin": true}' -H "content-type: application/json"
####################################################################################################################################################


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({"message": "a valid token is missing"})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Potrebitel.query.filter_by(id=data['id']).first()
        except:
            return jsonify({"message": "token is invalid"})

        return f(current_user, *args, **kwargs)
    return decorator


class Potrebitel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    admin = db.Column(db.Boolean)


class PotrebitelShcema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Potrebitel
        load_instance = True


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('potrebitel.id'), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    book_prize = db.Column(db.Integer)


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


class AddPotrebitel(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = Potrebitel(username=data['username'], password=hashed_password, admin=data['admin'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'registered successfully'})

    def get(self):
        q = Potrebitel.query.all()
        schema = PotrebitelShcema(many=True)
        print(q)
        return schema.dump(q)


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify!', 401, {'Authentication': 'login required'})

    user = Potrebitel.query.filter_by(username=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})



@app.route('/')
@token_required
def check_secret():
    return {"message": "This is a secret page :)"}


api.add_resource(ShowAllUsers, '/user')
api.add_resource(UserShow, '/user/<id>')
api.add_resource(AddPotrebitel, '/user/add_new')

if __name__ == '__main__':
    app.run(debug=True)
