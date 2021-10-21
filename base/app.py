from flask import request, render_template

from config import app
from config.models import TownModel


@app.route('/')
def hello():
    return "Test if work"


@app.route('/<name>')
def hello_name(name):
    return f"Hello {name}"


@app.route('/towns', methods=['GET', 'POST'])
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


@app.route('/show_towns')
def show_towns_in_template():
    return render_template('show_all_towns.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
