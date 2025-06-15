from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from server.controllers.restaurant_controller import restaurant_bp
    from server.controllers.pizza_controller import pizza_bp
    from server.controllers.restaurant_pizza_controller import restaurant_pizza_bp
    from server.controllers.json_data_controller import json_data_bp

    app.register_blueprint(restaurant_bp, url_prefix='/restaurants')
    app.register_blueprint(pizza_bp, url_prefix='/pizzas')
    app.register_blueprint(restaurant_pizza_bp, url_prefix='/restaurant_pizzas')
    app.register_blueprint(json_data_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Pizza Restaurants API"})

    @app.errorhandler(404)
    def not_found(e):
        # Fix duplicate error message issue by returning a clean JSON response
        return jsonify({"error": "Resource not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    # Removed app.run() to use 'flask run' command instead
