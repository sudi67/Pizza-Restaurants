from server.app import create_app
from server.models.restaurant import Restaurant

app = create_app()

with app.app_context():
    restaurants = Restaurant.query.all()
    print(restaurants)
