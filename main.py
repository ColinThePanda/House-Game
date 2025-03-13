from floor import Floor
from vector import Vector
from house import House
from game import Game
from tile import Tile, TileType
from data_manager import DataManager
from data import SaveData
import os
import sys
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.box import Box
import time
import keyboard
import math
from shop import Shop
# Import UI functions from ui.py
from ui import (
    clear_console, 
    run_game_interface, 
    game_setup_interface, 
    main_menu, 
    show_selection_interface,
    SelectionOption,
    handle_shop_interface,
    display_win_screen
)

def calculate_gold(game: Game):
    house: House = game.house
    total_tiles: int = house.total_floors * house.floors[0].size.x * house.floors[0].size.y
    base_gold = round((10 + 5 * math.log2(1 + total_tiles) + (total_tiles / 4) * (1 - math.exp(-total_tiles / 100))) * (1 - (int(game.reveal_diagonals)) * 0.5))
    
    # Apply gold multiplier from items
    return game.update_gold_calculation(base_gold)

def check_win(game: Game):
    current_floor: Floor = game.house.floors[game.current_floor - 1]
    if current_floor.vault:
        if game.player.position.x == current_floor.vault.position.x and game.player.position.y == current_floor.vault.position.y:
            if game.player.has_key:
                return True
    return False

def start_game():
    game : Game = game_setup_interface()
    game_won : bool = run_game_interface(game)
    if game_won: 
        pass
        #display_win_screen(game, 5)
    game.save_data()

def start_shop():
    clear_console()
    shop = Shop()
    handle_shop_interface(shop)
    shop.data_manager.save_data(shop.data)

def main():
    while True:
        #main_menu()
        # Display main menu
        menu_options = [
            SelectionOption(name="Play Game", description="Start a new house exploration"),
            SelectionOption(name="Shop", description="Buy upgrades and items"),
            SelectionOption(name="Exit", description="Quit the game")
        ]
        
        choice = show_selection_interface(
            title="""[bold blue]
╔═╗╦ ╦╔═╗╦  ╔═╗╦═╗╔═╗╦═╗  ╦ ╦╔═╗╦ ╦╔═╗╔═╗
║╣ ╚╦╝╠═╝║  ║ ║╠╦╝║╣ ╠╦╝  ╠═╣║ ║║ ║╚═╗║╣ 
╚═╝ ╩ ╩  ╩═╝╚═╝╩╚═╚═╝╩╚═  ╩ ╩╚═╝╚═╝╚═╝╚═╝
[/bold blue]""",
            options=menu_options,
            initial_index=0,
            header_text="Welcome to Explorer House! What would you like to do?",
            footer_text="Use arrow keys to navigate and Enter to select",
            cancel_allowed=False
        )
        
        if choice == "Play Game":
            start_game()
        elif choice == "Shop":
            start_shop()
        elif choice == "Exit":
            print("Thanks for playing!")
            break
        else:
            # Fallback if something goes wrong
            choice_num = int(input("Do you want to 1. Play the game, 2. Go to the shop, 3. Exit: "))
            if choice_num == 1:
                start_game()
            elif choice_num == 2:
                start_shop()
            elif choice_num == 3:
                print("Thanks for playing!")
                break
    
if __name__ == "__main__":
    main()