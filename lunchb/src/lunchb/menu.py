from dataclasses import dataclass
from datetime import date

@dataclass
class Menu:
    title: str
    ingredients: str
    date: date
