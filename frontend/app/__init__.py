from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from app.config import Config

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app import routes, models


# def create_app():
#     app = Flask(__name__)
#     return app
