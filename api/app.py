from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/create_db')
def create_db():
    return {'message': 'Database was created'}


if __name__ == '__main__':
    app.run(debug=True)
