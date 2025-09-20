from flask import Flask, abort
from lunchb.restaurants import Restaurant
from datetime import date
from dataclasses import asdict

app = Flask(__name__)

available_restaurants = {r.name: r for r in Restaurant.__subclasses__()}
menu_cache = {}
@app.route('/list-restaurants', methods = ['GET'])
def list_restaurants():
    return [{"name": r.name, "url": r.url} for r in available_restaurants.values()]

@app.route('/menu/<string:restaurant_name>/<string:day>', methods = ['GET'])
def list_menus(restaurant_name, day):
    global current_day
    if day == "today" and restaurant_name in available_restaurants:
        if restaurant_name in menu_cache and menu_cache[restaurant_name]["last_updated"] == date.today():
            return menu_cache[restaurant_name]["data"]
        restaurant = available_restaurants[restaurant_name]
        menus = restaurant().fetch_menus()
        menus = filter(lambda x: x.date == date.today(), menus)
        menus = list(map(asdict, menus))
        # update cache
        menu_cache[restaurant_name] = {"data": menus, "last_updated": date.today()}
        return menus
    abort(404) # TODO: better error handling

def main():
    app.run(host="0.0.0.0", port=8218)

if __name__ == '__main__':
    main()
