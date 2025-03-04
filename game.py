from house import House
from player import Player
from vector import Vector
from floor import Floor
from tile import Tile, TileType
import random
from rich.console import Console
from rich.table import Table
from rich import box

class Game():
    def __init__(self, floor_size : Vector, floors : int):
        self.house = House(floor_size, floors)
        self.player = Player(self.get_player_start())
        self.current_floor : int = 1
    
    def get_player_start(self):
        tiles = []
        # Only check the first floor
        first_floor = self.house.floors[0]
        for tile in first_floor.tiles:
            if tile.type == TileType.BASIC:
                tiles.append(tile)
        
        if tiles:
            return random.choice(tiles).position
        else:
            # Fallback in case no BASIC tiles are found (though unlikely)
            return Vector(0, 0)
    
    def move_player(self, position : Vector):
        print(position.xy)
        self.player.move(position)
        current_floor = self.house.floors[self.current_floor - 1]
        if current_floor.up_stair:
            if self.player.position.xy == current_floor.up_stair.position.xy:
                self.player.can_move_up = True
        if current_floor.down_stair:
            if self.player.position.xy == current_floor.down_stair.position.xy:
                self.player.can_move_down = True
    
    def print_floor(self, floor : int):
        console = Console()

        TILE_COLORS = {
            TileType.BASIC: "white",
            TileType.STAIR_UP: "green",
            TileType.STAIR_DOWN: "red",
            TileType.VAULT: "yellow",
        }

        floor = self.house.floors[floor-1]
        table = Table(title=f"Floor #{floor.index + 1}", box=box.HEAVY_EDGE)

        # Add column headers (including an extra for row numbers)
        table.add_column("#", justify="center", style="bold")
        for i in range(floor.size.x):
            table.add_column(str(i + 1), justify="center", style="bold")

        # Add rows with row headers and tile names in color
        for y in range(floor.size.y):
            row = [str(y + 1)]  # First column with row number
            for tile in floor.tiles[y * floor.size.x : (y + 1) * floor.size.x]:
                if self.player.position == tile.position:
                    tile_color = "blue"
                else:
                    tile_color = TILE_COLORS.get(tile.type, "white")
                row.append(f"[{tile_color}]{tile.name}[/]")  # Apply Rich color formatting
            table.add_row(*row)

        console.print(table)
        console.print(self.player.position.xy)
    
