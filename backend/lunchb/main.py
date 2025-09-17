from flask import Flask, abort
from lunchb.restaurants import Restaurant
from datetime import date
from dataclasses import asdict

app = Flask(__name__)

rests = {r.name: r for r in Restaurant.__subclasses__()}
cache = {}
current_day = date.today()
@app.route('/list-restaurants', methods = ['GET'])
def list_restaurants():
    return [{"name": r.name, "url": r.url} for r in rests.values()]

@app.route('/menu/<string:restaurant_name>/<string:day>', methods = ['GET'])
def list_menus(restaurant_name, day):
    global current_day
    if day == "today" and restaurant_name in rests:
        if restaurant_name in cache and current_day == date.today():
            return cache[restaurant_name]
        restaurant = rests[restaurant_name]
        menus = restaurant().fetch_menus()
        menus = filter(lambda x: x.date == date.today(), menus)
        menus = list(map(asdict, menus))
        # update cache
        cache[restaurant_name] = menus
        current_day = date.today()
        return menus
    abort(404) # TODO: better error handling

def main():
    app.run(host="0.0.0.0", port="8218")

if __name__ == '__main__':
    main()
