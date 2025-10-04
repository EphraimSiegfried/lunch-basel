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
        if today.weekday() >= 5:
            return []

        # fetch pdf and set up parser object
        response = requests.get(self.url)
        file_hash = hash(response.content)
        pdf_name = f"{file_hash}.pdf"
        with open(pdf_name, "wb") as file:
            file.write(response.content)
        pdf_reader = PdfReader(pdf_name)
        page = pdf_reader.pages[0]

        # extract text
        menus = []
        print(page.extract_text())

        # def v1(text,cm,tm,font_dict,font_size):
        #     y = tm[5]
        #     x = tm[4]
        #     if 350 < y < 420 :
        #         if 95 < x < 250:
        #             menus.append(text)
        #         else:
        #             menus.append(text)
        #
        # page.extract_text(visitor_text=v1)
        print(menus)

        #clean up
        os.remove(pdf_name)
        return menus

def from_compass_group(url):
    # return nothing if it's a weekend
    if date.today().weekday() >= 5:
        return []
    menus = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    menu_entries = soup.find_all("li", class_ = "menuline")
    menu_entries = list(map(lambda x: x.parent.parent, menu_entries))
    for entry in menu_entries:
        menu_title = entry.find("h3").text.strip()
        ingredients = entry.find("p")
        ingredients = ingredients.text.strip() if ingredients != None else ""
        menus.append(Menu(menu_title, ingredients, date.today()))
    return menus

if __name__ == "__main__":
    CantinaE9().fetch_menus()
