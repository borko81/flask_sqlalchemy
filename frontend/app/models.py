from datetime import datetime

from app import db
from app import ma
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        self.set_password(self.password_hash)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # username = db.Column(db.String(120), default=User.query.filter_by(id=user_id).first().username)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return self.body[:10]


class PostSchema(ma.SQLAlchemySchema):
    username = 'users_id'

    class Meta:
        model = Post

    id = ma.auto_field()
    body = ma.auto_field()
    timestamp = ma.auto_field()
    user_id = ma.auto_field()
    user_id.username = ma.auto_field()


class UserSchema(ma.SQLAlchemyAutoSchema):
    posts = ma.Nested(PostSchema, many=True)

    class Meta:
        model = User
        load_instance = True
        # include_relationships = True # ->Add only id!!!


class UserSchemaWithoutPost(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()


class PostSchemaWithUsername(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        load_relationships = True

    user_id = ma.auto_field()
    # username = ma.Method(User.query.filter_by(id=user_id))
