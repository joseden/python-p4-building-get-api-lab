#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "name" : bakery.name,
            "id" : bakery.id,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at,
        }

        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id==id).first() # Using get() for primary key lookup is more concise
    if bakery:
        return jsonify(bakery.to_dict()), 200  # Corrected syntax for jsonify and HTTP status code
    else:
        return jsonify({"error": "Bakery not found"}), 404  # Corrected syntax for jsonify and HTTP status code
     
    
@app.route('/baked_goods')
def get_baked_goods():
    baked_goods = []
    for baked_good in BakedGood.query.all():
        baked_good_dict = {
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "created_at": baked_good.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Convert to string representation
        }
        baked_goods.append(baked_good_dict)

    response = make_response(
        jsonify(baked_goods),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    if baked_goods_by_price:
        baked_goods_dicts = [baked_good.to_dict() for baked_good in baked_goods_by_price]
        return jsonify(baked_goods_dicts), 200
    else:
        return jsonify({"error": "Baked goods not found"}), 404
    
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    if most_expensive_baked_good:
        return jsonify(most_expensive_baked_good.to_dict()), 200
    else:
        return jsonify({"error": "Price not found"}), 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
