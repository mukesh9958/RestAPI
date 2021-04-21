

from flask import Flask 

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/cart"

mongo = PyMongo(app)


@app.route('/add', methods = ['POST'])
def add_product():
    _json = request.json
    _name = _json['name']
    _quantity = _json['quantity']
    _price = _json['price']
    _description = _json['description']

    if _name and _quantity and _price and _description and request.method == 'POST':

        id = mongo.db.product.insert({'name': _name,'quantity': _quantity,'price': _price, 'description': _description})
        
        resp = jsonify("product added successfuly")

        resp.status_code = 200

        return resp

    
    else:
        return not_found()


@app.route('/cart')
def show_product():
    cart = mongo.db.product.find()
    resp = dumps(cart)
    return resp


@app.route('/cart/<id>')
def product(id):
    cart=mongo.db.product.find_one({'_id':ObjectId(id)})
    resp = dumps(cart)
    return resp


@app.route('/delete/<id>', methods = ['DELETE'])
def delete_product(id):
    mongo.db.product.delete_one({'_id': ObjectId(id)})
    resp = jsonify("Product deleted successfully")

    resp.status_code = 200
    return resp


@app.route('/update/<id>', methods = ['PUT'])
def update_product(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _quantity = _json['quantity']
    _price = _json['price']
    _description = _json['description']

    if _name and _quantity and _price and _description and request.method == 'PUT':

        mongo.db.product.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set': {'name': _name, 'quantity': _quantity, 'price': _price, 'description': _description}})

        resp= jsonify("product updated successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found'+request.url()
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(debug=True)

