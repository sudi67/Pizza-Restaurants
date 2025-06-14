from flask import Blueprint, jsonify, request
from server.app import db
from server.models.restaurant import Restaurant

restaurant_bp = Blueprint('restaurant_bp', __name__)

@restaurant_bp.route('', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    print(f"DEBUG: Retrieved restaurants count: {len(restaurants)}")  # Debug log
    return jsonify([r.to_dict() for r in restaurants]), 200

@restaurant_bp.route('/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict()), 200

@restaurant_bp.route('/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

@restaurant_bp.route('/<int:id>', methods=['PUT'])
def update_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    data = request.get_json()
    errors = []
    name = data.get('name')
    address = data.get('address')
    if not name or not isinstance(name, str) or name.strip() == '':
        errors.append('Name is required and must be a non-empty string.')
    if not address or not isinstance(address, str) or address.strip() == '':
        errors.append('Address is required and must be a non-empty string.')
    if errors:
        return jsonify({'errors': errors}), 400
    restaurant.name = name.strip()
    restaurant.address = address.strip()
    db.session.commit()
    return jsonify({
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address
    })
