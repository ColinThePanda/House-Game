from tile import TileType, Tile
from vector import Vector
from typing import List
import random

class Floor():
    def __init__(self, floor_index : int, size : Vector, total_floors : int, previous_floor : "Floor" = None):
        self.index : int = floor_index
        self.size : Vector = size
        self.tiles : List[Tile] = []
        self.previous_floor : "Floor" = previous_floor
        self.down_stair : Tile = None
        self.up_stair : Tile = None
        self.vault : Tile = None
        self.key : Tile = None
        self.generate_floor(total_floors)
    
    def generate_floor(self, total_floors : int):
        self.tiles = []
        for x in range(self.size.x):
            for y in range(self.size.y):
                self.tiles.append(Tile(TileType.BASIC, "Basic Tile", Vector(x, y)))
        
        if self.index == total_floors - 1:
            self.vault = self.place_tile(TileType.VAULT, "Vault")
        if total_floors == 1:
            return
        if self.index != 0:
            self.down_stair = self.place_down_stair()
        if self.index < total_floors - 1:
            self.up_stair = self.place_tile(TileType.STAIR_UP, "Stair Up")
    
    def place_tile(self, tile_type : TileType, name : str):
        tiles = []
        for tile in self.tiles:
            if tile.type == TileType.BASIC:
                tiles.append(tile)
                #print(tile.name, tile.type, tile.position.x + 1, tile.position.y + 1)
        tile = random.choice(tiles)
        #print("\n")
        #print(tile.name, tile.type, tile.position.x + 1, tile.position.y + 1)
        tile_index = self.tiles.index(tile)
        self.tiles[tile_index] = Tile(tile_type, name, tile.position)
        return self.tiles[tile_index]
    
    def place_down_stair(self):
        if self.previous_floor:
            if self.previous_floor.up_stair:
                up_stair = self.previous_floor.up_stair
            else:
                return
        else:
            return
        position = up_stair.position
        for tile in self.tiles:
            #print(position.x, position.y, tile.position.x, tile.position.y)
            if tile.position.x == position.x and tile.position.y == position.y:
                tile_index = self.tiles.index(tile)
                #print("Down Stair")
                self.tiles[tile_index] = Tile(TileType.STAIR_DOWN, "Stair Down", position)
                return self.tiles[tile_index]
        