from flask import jsonify

from config import app, api
from config.tax_resourse import AllTaxResurse, TaxResurse

api.add_resource(AllTaxResurse, '/tax')
api.add_resource(TaxResurse, '/tax/<_id>')


@app.route("/server_alive")
def some_json():
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)