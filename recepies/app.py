from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipie.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['JWT_SECRET_KEY'] = 'secret-string'
db = SQLAlchemy(app)


class RecepiIngedient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recepi.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Integer)
    recepi = db.relationship("Recepi", backref='recepi')
    ingredient = db.relationship("Ingredient", backref='ingredient')


class Recepi(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), index=True)
    price = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return self.name


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit = db.Column(db.Integer, db.ForeignKey('units.id'))
    name = db.Column(db.String(100))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"{self.name} {self.unit}"


class Units(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
