from flask import Flask

from many_to_one import Group, app


@app.route('/')
def index():
    a = Group.query.filter_by(id=1).first()
    return {'name': a.name}


if __name__ == '__main__':
    app.run(debug=True)
