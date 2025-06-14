from flask import Blueprint, jsonify, request
from server.app import db
from server.models.pizza import Pizza

pizza_bp = Blueprint('pizza_bp', __name__)

@pizza_bp.route('', methods=['GET'])
def get_pizzas():
    name_filter = request.args.get('name')
    query = Pizza.query
    if name_filter:
        query = query.filter(Pizza.name.ilike(f'%{name_filter}%'))
    pizzas = query.all()
    return jsonify([p.to_dict() for p in pizzas]), 200

@pizza_bp.route('/<int:id>', methods=['GET'])
def get_pizza(id):
    pizza = Pizza.query.get(id)
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    return jsonify(pizza.to_dict()), 200

@pizza_bp.route('/<int:id>', methods=['PUT'])
def update_pizza(id):
    pizza = Pizza.query.get(id)
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    data = request.get_json()
    errors = []
    name = data.get('name')
    ingredients = data.get('ingredients')
    if not name or not isinstance(name, str) or name.strip() == '':
        errors.append('Name is required and must be a non-empty string.')
    if not ingredients or not isinstance(ingredients, str) or ingredients.strip() == '':
        errors.append('Ingredients are required and must be a non-empty string.')
    if errors:
        return jsonify({'errors': errors}), 400
    pizza.name = name.strip()
    pizza.ingredients = ingredients.strip()
    db.session.commit()
    return jsonify({
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    })
