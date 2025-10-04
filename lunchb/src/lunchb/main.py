import os
from dataclasses import asdict
from datetime import date

from flask import Flask, abort
# Import the gunicorn application class
from gunicorn.app.base import BaseApplication

from lunchb.restaurants import Restaurant

app = Flask(__name__)

available_restaurants = {r.name: r for r in Restaurant.__subclasses__()}
menu_cache = {}


@app.route("/list-restaurants", methods=["GET"])
def list_restaurants():
    return [{"name": r.name, "url": r.url} for r in available_restaurants.values()]


@app.route("/menu/<string:restaurant_name>/<string:day>", methods=["GET"])
def list_menus(restaurant_name, day):
    # global current_day is not needed here
    if day == "today" and restaurant_name in available_restaurants:
        if (
            restaurant_name in menu_cache
            and menu_cache[restaurant_name]["last_updated"] == date.today()
        ):
            return menu_cache[restaurant_name]["data"]
        restaurant = available_restaurants[restaurant_name]
        menus = restaurant().fetch_menus()
        menus = filter(lambda x: x.date == date.today(), menus)
        menus = list(map(asdict, menus))
        # update cache
        menu_cache[restaurant_name] = {"data": menus, "last_updated": date.today()}
        return menus
    abort(404)  # TODO: better error handling


# ----------------------------------------------------------------------
# Gunicorn Setup
# ----------------------------------------------------------------------


class StandaloneApplication(BaseApplication):
    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run_gunicorn():
    options = {
        "bind": f"0.0.0.0:{os.environ["PORT"] if "PORT" in os.environ else "8218"}",
        "workers": 4,
        "wsgi_app": "main:app",
        "loglevel": "info",
    }

    StandaloneApplication(app, options).run()


def main():
    run_gunicorn()

    # app.run(host="0.0.0.0", port=8218)


if __name__ == "__main__":
    main()
