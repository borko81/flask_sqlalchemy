from app import app
from app.forms import LoginForm
from flask import flash, render_template, redirect, url_for, request


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
