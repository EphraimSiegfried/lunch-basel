import os
from bs4 import BeautifulSoup
from lunchb.menu import Menu
import requests
from datetime import date
from pypdf import PdfReader
from datetime import date, timedelta
from itertools import batched

class Restaurant():
    name = ""
    url = ""
    def fetch_menus(self) -> list[Menu]:
        return []

class Bacells(Restaurant):
    name = "BaCells"
    url = "https://clients.compass-group.ch/unibas-biozentrum/de/BaCells"
    def fetch_menus(self):
        return from_compass_group(self.url)

class Bernoulli(Restaurant):
    name = "Bernoulli"
    url = "https://clients.compass-group.ch/unibas-bernoulli/de/Mensa%20Bernoulli"
    def fetch_menus(self):
        return from_compass_group(self.url)

class CantinaE9(Restaurant):
    name = "Cantina E9"
    url = "https://www.cantina-e9.ch/images/menuplan/menuplan.pdf"
    def fetch_menus(self):
        today = date.today()
        # return nothing if it's a weekend
        if today.weekday() <= 5:
            return []
        response = requests.get(self.url)
        file_hash = hash(response.content)
        pdf_name = f"{file_hash}.pdf"
        with open(pdf_name, "wb") as file:
            file.write(response.content)
        pdf_reader = PdfReader(pdf_name)
        page = pdf_reader.pages[0]
        entries = page.extract_text().splitlines()
        # TODO: Better parsing
        entries = filter(lambda x: x != ', ' and not x.isspace() and "(kein Menüsalat)" not in x, entries)
        entries = map(lambda x: x.strip(), entries)
        entries = list(entries)[3:-6]
        entries = list(batched(entries, n=2))

        today = date.today()
        current_d = today - timedelta(days=today.weekday())

        menus = []
        for ((m1, i1), (m2, i2)) in batched(entries, n=2):
            menus.append(Menu(m1, i1, current_d))
            menus.append(Menu(m2, i2, current_d))
            current_d += timedelta(days=1)
        os.remove(pdf_name)
        return menus

def from_compass_group(url):
    today = date.today()
    # return nothing if it's a weekend
    if today.weekday() <= 5:
        return []
    menus = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    menu_entries = soup.find_all("li", class_ = "menuline")
    menu_entries = list(map(lambda x: x.parent.parent, menu_entries))
    for entry in menu_entries:
        menu_title = entry.find("h3").text.strip()
        ingredients = entry.find("p").text.strip()
        menus.append(Menu(menu_title, ingredients, date.today()))
    return menus
