from flask import jsonify

from config import app, api
from config.tax_resourse import AllTaxResurse, TaxResurse
from config.user_resourse import UserResourse, UserJWT
from config.car_resourse import CarResourse, CarsResourse

api.add_resource(AllTaxResurse, '/tax')
api.add_resource(TaxResurse, '/tax/<_id>')

api.add_resource(UserResourse, '/users')
api.add_resource(UserJWT, '/users/jwt')

api.add_resource(CarsResourse, '/cars')
api.add_resource(CarResourse, '/car/<_id>')


@app.route("/server_alive")
def some_json():
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)