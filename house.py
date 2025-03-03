from floor import Floor
from vector import Vector
from tile import TileType, Tile
import random
from rich.console import Console
from rich.table import Table
from rich import box

class House():
    def __init__(self, floor_size : Vector, total_floors : int):
        self.size : Vector = floor_size
        self.total_floors : int = total_floors
        self.floors : list = []
        self.generate_house()
    
    def generate_house(self):
        for i in range(self.total_floors):
            if i == 0:
                self.floors.append(Floor(i, self.size, self.total_floors))
            else:
                self.floors.append(Floor(i, self.size, self.total_floors, self.floors[i - 1]))

    def print_tiles(self):
        console = Console()

        TILE_COLORS = {
            TileType.BASIC: "white",
            TileType.STAIR_UP: "green",
            TileType.STAIR_DOWN: "red",
            TileType.VAULT: "yellow",
        }

        for floor in self.floors:
            table = Table(title=f"Floor #{floor.index + 1}", box=box.HEAVY_EDGE)

            # Add column headers (including an extra for row numbers)
            table.add_column("#", justify="center", style="bold")
            for i in range(floor.size.x):
                table.add_column(str(i + 1), justify="center", style="bold")

            # Add rows with row headers and tile names in color
            for y in range(floor.size.y):
                row = [str(y + 1)]  # First column with row number
                for tile in floor.tiles[y * floor.size.x : (y + 1) * floor.size.x]:
                    tile_color = TILE_COLORS.get(tile.type, "white")
                    row.append(f"[{tile_color}]{tile.name}[/]")  # Apply Rich color formatting
                table.add_row(*row)

            console.print(table)
