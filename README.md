# Lunch Basel

Website which displays the daily menu of all the canteens/restaurants I like.

## Docker Deployment

Deploy with `docker compose up -d`. You can access the website locally at
http://localhost:3000.

## Modifications

To add a restaurant you only have to write a class which inherits from the
Restaurant class and write all it's methods
[here](./backend/lunchb/restaurants.py).
