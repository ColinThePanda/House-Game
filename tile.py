from enum import Enum
from vector import Vector

class TileType(Enum):
    BASIC = 0
    STAIR_UP = 1
    STAIR_DOWN = 2
    VAULT = 3

class Tile():
    def __init__(self, tile_type : TileType, name : str, position : Vector = None):
        self.type : TileType = tile_type
        self.name : str = name
        self.position : Vector = position

    def __str__(self):
        return self.name
    
    def print_info(self):
        print(self.name, self.type, self.position.x + 1, self.position.y + 1)

