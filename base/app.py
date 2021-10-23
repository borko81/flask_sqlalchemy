from flask import request, render_template, session, redirect, url_for, flash

from config import app
from config.models import TownModel, UserModel


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            u = UserModel.find_user_by_name(username)
            if u and u.check_password(password):
                session['username_login'] = username
                return redirect(url_for('hello'))
            return f'{username} is not authenticated'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(password, password2)
        if not password2 == password:
            flash('Password did not much')
            return redirect(url_for('register'))
        u = UserModel(name=username, password=password)
        u.hashed_password(u.password)
        u.save()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/')
def hello():
    if 'username_login' in session:
        return "Test if work"
    return 'Not login'


@app.route('/username/<name>')
def hello_name(name):
    return f"Hello {name}"


@app.route('/towns', methods=['GET', 'POST', 'DELETE'])
def show_towns():
    if request.method == 'GET':
        towns = TownModel.query.all()
        data = {'towns': []}
        for t in towns:
            data['towns'].append({'id': t.id, 'name': t.name})
        return data, 200
    elif request.method == 'POST':
        data = request.get_json()
        name = data['name']
        t = TownModel(name=name)
        t.save()
        return {'message': 'New town was created successfully'}, 201
    elif request.method == 'DELETE':
        data = request.get_json()
        name = data['name']
        t = TownModel.find_from_name(name)
        t.delete()



@app.route('/show_towns', methods=['GET', 'POST'])
def show_towns_in_template():
    return render_template('show_all_towns.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
