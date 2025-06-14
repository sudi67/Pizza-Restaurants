from flask import Blueprint, request, jsonify
from server.app import db
from server.models.restaurant_pizza import RestaurantPizza

restaurant_pizza_bp = Blueprint('restaurant_pizza_bp', __name__)

@restaurant_pizza_bp.route('', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    errors = []
    if price is None:
        errors.append("Price is required")
    else:
        try:
            price = int(price)
            if price < 1 or price > 30:
                errors.append("Price must be between 1 and 30")
        except ValueError:
            errors.append("Price must be an integer")

    if pizza_id is None:
        errors.append("pizza_id is required")
    if restaurant_id is None:
        errors.append("restaurant_id is required")

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(new_rp)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

    return jsonify(new_rp.to_dict()), 201

@restaurant_pizza_bp.route('/<int:id>', methods=['PUT'])
def update_restaurant_pizza(id):
    rp = RestaurantPizza.query.get(id)
    if not rp:
        return jsonify({"error": "RestaurantPizza not found"}), 404
    data = request.get_json()
    errors = []
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if price is None:
        errors.append("Price is required")
    else:
        try:
            price = int(price)
            if price < 1 or price > 30:
                errors.append("Price must be between 1 and 30")
        except ValueError:
            errors.append("Price must be an integer")

    if pizza_id is None:
        errors.append("pizza_id is required")
    if restaurant_id is None:
        errors.append("restaurant_id is required")

    if errors:
        return jsonify({"errors": errors}), 400

    rp.price = price
    rp.pizza_id = pizza_id
    rp.restaurant_id = restaurant_id
    db.session.commit()
    return jsonify(rp.to_dict())
