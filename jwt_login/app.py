from flask import Flask, make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jwt.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['JWT_SECRET_KEY'] = 'secret-string'
db = SQLAlchemy(app)
jwt = JWTManager(app)


# curl 127.0.0.1:5000/login -X POST -d '{"username": "borko", "password": "borko"}' -H "content-type: application/json"
# curl 127.0.0.1:5000/secret -H "Accept: application/json" -H "Authorization: Bearer token"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.get_json())
        try:
            data = request.get_json()
        except:
            return jsonify({"message": 'Enter credential!'})
        username = data['username']
        password = data['password']
        u = User.query.filter_by(username=username).first()
        if u is None or not u.check_password(password):
            return jsonify({'message': 'Credential is invalid!'}), 401
        access_token = create_access_token(identity=data['username'])
        return jsonify({'message': 'Looked good', "token": access_token})
    return jsonify({'message': 'Welcome to the login page!'})


@app.route('/secret')
@jwt_required()
def secret():
    return make_response({'message': 'The secret message'})


if __name__ == '__main__':
    app.run(debug=True)
