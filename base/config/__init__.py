from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
app.config.from_object("config.myconfig.Config")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret key"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
CORS(app)
app.config['DEBUG'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from config import models
