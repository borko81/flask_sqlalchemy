import json

from app import app
from app.forms import LoginForm
from flask import flash, render_template, redirect, url_for, request, jsonify, make_response

from app.models import Post, PostSchema, User, UserSchema, PostSchemaWithUsername, UserSchemaWithoutPost


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login success')
        return redirect(url_for('check_it_work'))
    return render_template('login.html', form=form)


@app.route('/check')
def check_it_work():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    user = {'username': 'Borko'}
    return render_template('index.html', **user, title="Check Page", posts=posts)


@app.route('/show_users')
def show_users():
    users = User.query.all()
    print(users)
    schema = UserSchemaWithoutPost(many=True)
    print(schema.dump(users))
    return jsonify(schema.dump(users))


@app.route('/show_posts')
def show_posts():
    post = Post.query.all()
    schema = PostSchemaWithUsername(many=True)
    return jsonify(schema.dump(post))


@app.route('/show_post/<id>')
def show_concret_post(id):
    post = Post.query.filter_by(user_id=id).first()
    user = User.query.filter_by(id=id).first().username
    schema = PostSchemaWithUsername()
    result = jsonify(schema.dump(post), {'username': user})
    return result