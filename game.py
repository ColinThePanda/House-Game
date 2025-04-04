from house import House
from player import Player
from vector import Vector
from floor import Floor
from tile import Tile, TileType
import random
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
from data_manager import DataManager
from typing import List, Dict
from effect import *
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print

class Game():
    def __init__(self, floor_size : Vector, floors : int):
            self.house: House = House(floor_size, floors)
            self.data_manager = DataManager()
            self.data = self.data_manager.load_data()
            self.player: Player = Player(self.get_player_start(), self.data.items)
            self.current_floor: int = 1
            self.reveal_diagonals: bool = False
            self.gold_multiplier = 1.0  # Default multiplier
            
            # Apply effects from items
            self.apply_item_effects()
            
            # Reveal tiles around the player's starting position
            self.reveal_tiles_around_player()

    
    def save_data(self):
        self.data_manager.save_data(self.data)
    
    def get_player_start(self):
        tiles : List[Tile] = []
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
        #if not self.is_valid_move(position):
        #    return
        self.player.move(position)
        
        # Reveal tiles around the player after moving
        self.reveal_tiles_around_player()
        
        current_floor : Floor = self.house.floors[self.current_floor - 1]
        if current_floor.up_stair:
            if self.player.position.x == current_floor.up_stair.position.x and self.player.position.y == current_floor.up_stair.position.y:
                self.player.can_move_up = True
            else:
                self.player.can_move_up = False
        else:
            self.player.can_move_up = False
        if current_floor.down_stair:
            if self.player.position.x == current_floor.down_stair.position.x and self.player.position.y == current_floor.down_stair.position.y:
                self.player.can_move_down = True
            else:
                self.player.can_move_down = False
        else:
                self.player.can_move_down = False
        if current_floor.key:
            if self.player.position.x == current_floor.key.position.x and self.player.position.y == current_floor.key.position.y:
                for tile in current_floor.tiles:
                    if tile.position.x == current_floor.key.position.x and tile.position.y == current_floor.key.position.y:
                        tile_index = current_floor.tiles.index(tile)
                
                current_floor.tiles[tile_index] = Tile(TileType.BASIC, "Basic Tile", current_floor.key.position)
                current_floor.key = None
                self.player.has_key = True
                self.reveal_tiles_around_player()
    
    def is_valid_move(self, position : Vector):
        if position.x < 0 or position.x >= self.house.size.x or position.y < 0 or position.y >= self.house.size.y:
            return False
        return True
    
    def move_floor(self, floor : int):
        if floor < 1 or floor > self.house.total_floors:
            return
        if floor > self.current_floor:
            self.player.can_move_up = False
            self.player.can_move_down = True
        if floor < self.current_floor:
            self.player.can_move_up = True
            self.player.can_move_down = False
        self.current_floor = floor
        self.house.floors[self.current_floor - 1].discovered = True
        self.reveal_tiles_around_player()
    
    def reveal_tiles_around_player(self):
        current_floor = self.house.floors[self.current_floor - 1]
        player_x, player_y = self.player.position.x, self.player.position.y
        
        # Mark tiles as found
        for tile in current_floor.tiles:
            # Reveal the tile the player is on
            if tile.position.x == player_x and tile.position.y == player_y:
                tile.found = True
            
            # Reveal adjacent tiles (up, down, left, right)
            elif (
                (tile.position.x == player_x and abs(tile.position.y - player_y) == 1) or  # up/down
                (tile.position.y == player_y and abs(tile.position.x - player_x) == 1)or   # left/right
                ((abs(tile.position.x - player_x) == 1 and abs(tile.position.y - player_y) == 1) and self.reveal_diagonals)  # diagonals
            ):
                tile.found = True
    
    def apply_item_effects(self):
        """Apply effects from all player items."""
        # Reset effect-based attributes before applying effects
        self.player.can_teleport = False
        
        # Apply effects that target the player or game
        for item in self.player.items:
            for effect in item.effects:
                if effect.type == EffectType.PLAYER:
                    effect.apply(self.player)
                elif effect.type == EffectType.GAME:
                    effect.apply(self)
        
        # After applying effects, update game state accordingly
        self.reveal_tiles_around_player()

    def update_gold_calculation(self, base_gold):
        """Apply gold multiplier from items."""
        if hasattr(self, 'gold_multiplier'):
            return int(base_gold * self.gold_multiplier)
        return base_gold

    def get_options(self):
        """Get all valid movement options for the current player position."""
        options: List[str] = []
        current_floor = self.house.floors[self.current_floor - 1]
        
        # Cardinal directions
        if self.player.position.y < current_floor.size.y - 1:
            options.append("up")
        if self.player.position.y > 0:
            options.append("down")
        if self.player.position.x > 0:
            options.append("left")
        if self.player.position.x < current_floor.size.x - 1:
            options.append("right")
        
        # Floor movement
        if self.player.can_move_up:
            options.append("move up")
        if self.player.can_move_down:
            options.append("move down")
        
        # Teleport option if player has the ability
        if hasattr(self.player, 'can_teleport') and self.player.can_teleport:
            options.append("teleport")
        
        options.append("exit")
        return options
    
    def get_current_floor(self):
        """Helper method to get the current floor object."""
        return self.house.floors[self.current_floor - 1]
    
    def get_discovered_floors(self):
        """Get list of all discovered floors."""
        return [floor for floor in self.house.floors if floor.discovered]
    
    def is_win_condition_met(self):
        """Check if the player has won."""
        current_floor = self.get_current_floor()
        if current_floor.vault:
            if (self.player.position.x == current_floor.vault.position.x and 
                self.player.position.y == current_floor.vault.position.y):
                if self.player.has_key:
                    return True
        return False
    
    def process_win(self):
        """Process win condition and add gold."""
        from main import calculate_gold  # Import calculation function
        gold_earned = calculate_gold(self)
        self.data.gold += gold_earned
        self.save_data()
        return gold_earned
    
    def print_floor(self, floor : int):
        console = Console()

        TILE_COLORS : Dict[TileType, str] = {
            TileType.BASIC: "white",
            TileType.STAIR_UP: "green",
            TileType.STAIR_DOWN: "red",
            TileType.VAULT: "yellow",
            TileType.KEY: "#FFAE42",
        }

        TILE_SYMBOLS : Dict[TileType, str] = {
            TileType.BASIC: "·",      # Middle dot for basic tiles
            TileType.STAIR_UP: "↑",   # Up arrow for stairs up
            TileType.STAIR_DOWN: "↓", # Down arrow for stairs down
            TileType.VAULT: "V",      # V for vault
            TileType.KEY: "K",        # K for key
        }

        floor : Floor = self.house.floors[floor-1]
        table : Table = Table(title=f"Floor #{floor.index + 1}", box=box.HEAVY_EDGE)

        # Add column headers (including an extra for row numbers)
        table.add_column("#", justify="center", style="bold")
        for x in range(floor.size.x):
            table.add_column(str(x + 1), justify="center", style="bold")

        # Process rows from highest y to lowest y (bottom-up)
        for y_idx in range(floor.size.y - 1, -1, -1):
            row = [str(y_idx + 1)]  # Row label shows actual y-coordinate (1-based)
            
            for x in range(floor.size.x):
                # Find the tile at the current (x, y) coordinate
                tile = next(tile for tile in floor.tiles if tile.position.x == x and tile.position.y == y_idx)
                
                if not tile.found:
                    # Display hidden tile as "?"
                    row.append("[#8B4513]?[/#8B4513]")  # Brown color
                else:
                    # Tile is visible, display with symbol instead of full name
                    if self.player.position == tile.position:
                        tile_color = "blue"
                        tile_symbol = "P"  # P for player
                    else:
                        tile_color = TILE_COLORS.get(tile.type, "white")
                        tile_symbol = TILE_SYMBOLS.get(tile.type, " ")
                    
                    row.append(f"[{tile_color}]{tile_symbol}[/]")  # Apply Rich color formatting
            
            table.add_row(*row)

        console.print(table)
        console.print(f"Player Position: ({self.player.position.x + 1}, {self.player.position.y + 1})")
        
        # Display legend
        legend = Table(title="Legend", box=box.SIMPLE)
        legend.add_column("Symbol", justify="center")
        legend.add_column("Meaning", justify="left")
        legend.add_row("[blue]P[/blue]", "Player")
        legend.add_row("[#8B4513]?[/#8B4513]", "Unexplored")
        for tile_type, symbol in TILE_SYMBOLS.items():
            color = TILE_COLORS.get(tile_type, "white")
            legend.add_row(f"[{color}]{symbol}[/{color}]", f"{tile_type.name.replace('_', ' ').title()}")
        
        console.print(legend)

