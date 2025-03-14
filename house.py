from floor import Floor
from vector import Vector
from tile import TileType, Tile
from typing import List
import random

class House():
    def __init__(self, floor_size : Vector, total_floors : int):
        self.size : Vector = floor_size
        self.total_floors : int = total_floors
        self.floors : List[Floor] = []
        self.generate_house()
    
    def generate_house(self):
        for i in range(self.total_floors):
            if i == 0:
                self.floors.append(Floor(i, self.size, self.total_floors))
                self.floors[0].discovered = True
            else:
                self.floors.append(Floor(i, self.size, self.total_floors, self.floors[i - 1]))
        
        floor : Floor = random.choice(self.floors)
        floor.key = floor.place_tile(TileType.KEY, "Key")

