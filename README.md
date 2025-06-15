# Pizza Restaurant API Challenge

## Overview
This project is a RESTful API for a Pizza Restaurant built using Flask. It follows the MVC pattern with SQLAlchemy for ORM and Flask-Migrate for database migrations.

## Project Structure
```
.
├── server/
│   ├── __init__.py
│   ├── app.py                # App setup
│   ├── config.py             # DB config
│   ├── models/               # Models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── restaurant.py
│   │   ├── pizza.py
│   │   └── restaurant_pizza.py
│   ├── controllers/          # Route handlers (Controllers)
│   │   ├── __init__.py
│   │   ├── restaurant_controller.py
│   │   ├── pizza_controller.py
│   │   └── restaurant_pizza_controller.py
│   ├── seed.py               # Seed data
├── migrations/
├── challenge-1-pizzas.postman_collection.json
└── README.md
```

## Setup Instructions

### Create virtual environment and install packages
```bash
pipenv install flask flask_sqlalchemy flask_migrate
pipenv shell
```

### Database setup
```bash
export FLASK_APP=server/app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Seed the database
```bash
python server/seed.py
```

## Routes Summary

### Restaurants
- `GET /restaurants`  
  Returns a list of all restaurants.

- `GET /restaurants/<int:id>`  
  Returns details of a single restaurant and its pizzas.  
  If not found → `{ "error": "Restaurant not found" }` with 404

- `DELETE /restaurants/<int:id>`  
  Deletes a restaurant and all related RestaurantPizzas.  
  If successful → 204 No Content  
  If not found → `{ "error": "Restaurant not found" }` with 404

### Pizzas
- `GET /pizzas`  
  Returns a list of pizzas.

### RestaurantPizzas
- `POST /restaurant_pizzas`  
  Creates a new RestaurantPizza.  
  Request JSON:  
  ```json
  { "price": 5, "pizza_id": 1, "restaurant_id": 3 }
  ```  
  Success response:  
  ```json
  {
    "id": 4,
    "price": 5,
    "pizza_id": 1,
    "restaurant_id": 3,
    "pizza": { "id": 1, "name": "Emma", "ingredients": "Dough, Tomato Sauce, Cheese" },
    "restaurant": { "id": 3, "name": "Kiki's Pizza", "address": "address3" }
  }
  ```  
  Error response:  
  ```json
  { "errors": ["Price must be between 1 and 30"] }
  ```  
  With 400 Bad Request

## Validation Rules
- `RestaurantPizza.price` must be an integer between 1 and 30 inclusive.

## Postman Usage
- Import the provided `challenge-1-pizzas.postman_collection.json` into Postman.
- Test each route using the collection.

## Notes
- Deleting a restaurant cascades to delete all related RestaurantPizzas.
- The API follows RESTful principles and returns appropriate HTTP status codes.
