from typing import List
from item import Item

class SaveData:
    def __init__(self):
        self.gold = 0
        self.items : List[Item] = []
