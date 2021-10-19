from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from models import Product, Group, db

app = Flask(__name__)
ma = Marshmallow(app)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Product': Product, 'Group': Group}


if __name__ == '__main__':
    app.run(debug=True)
