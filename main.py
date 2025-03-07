from floor import Floor
from vector import Vector
from house import House
from game import Game
from tile import Tile, TileType
import os
import sys
from rich.console import Console
from rich.text import Text
import time


def game_loop(game : Game):
    
    console = Console()
    
    # Display the current floor
    game.print_floor(game.current_floor)
    
    # Get options and color-code them
    options = game.get_options()
    
    # Define color mapping for each option
    option_colors = {
        "up": "blue",
        "down": "blue",
        "left": "blue",
        "right": "blue",
        "move up": "green",
        "move down": "red",
        "exit": "yellow"
    }
    
    # Create colored text for each option
    colored_options = []
    for option in options:
        color = option_colors.get(option, "white")
        colored_options.append(f"[{color}]{option}[/{color}]")
    
    # Display the prompt with colored options
    console.print(f"What do you want to do? ({', '.join(colored_options)})")
    
    # Get player input
    move = input("Enter your choice: ")
    
    if move == "exit":
        return False
    if move == "up":
        game.move_player(Vector(game.player.position.x, game.player.position.y + 1))
    if move == "down":
        game.move_player(Vector(game.player.position.x, game.player.position.y - 1))
    if move == "left":
        game.move_player(Vector(game.player.position.x - 1, game.player.position.y))
    if move == "right":
        game.move_player(Vector(game.player.position.x + 1, game.player.position.y))
    if move == "move up":
        game.move_floor(game.current_floor + 1)
    if move == "move down":
        game.move_floor(game.current_floor - 1)

    if check_win(game):
        clear_console()
        print("""
 .----------------.  .----------------.  .----------------.   .----------------.  .----------------.  .-----------------. .----------------. 
| .--------------. || .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. || .--------------. |
| |  ____  ____  | || |     ____     | || | _____  _____ | | | | _____  _____ | || |     _____    | || | ____  _____  | || |      _       | |
| | |_  _||_  _| | || |   .'    `.   | || ||_   _||_   _|| | | ||_   _||_   _|| || |    |_   _|   | || ||_   \|_   _| | || |     | |      | |
| |   \ \  / /   | || |  /  .--.  \  | || |  | |    | |  | | | |  | | /\ | |  | || |      | |     | || |  |   \ | |   | || |     | |      | |
| |    \ \/ /    | || |  | |    | |  | || |  | '    ' |  | | | |  | |/  \| |  | || |      | |     | || |  | |\ \| |   | || |     | |      | |
| |    _|  |_    | || |  \  `--'  /  | || |   \ `--' /   | | | |  |   /\   |  | || |     _| |_    | || | _| |_\   |_  | || |     |_|      | |
| |   |______|   | || |   `.____.'   | || |    `.__.'    | | | |  |__/  \__|  | || |    |_____|   | || ||_____|\____| | || |     (_)      | |
| |              | || |              | || |              | | | |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'   '----------------'  '----------------'  '----------------'  '----------------'  
""")
        game.print_floor(game.current_floor)
        return False

    return True

def check_win(game : Game):
    current_floor : Floor = game.house.floors[game.current_floor - 1]
    if current_floor.vault:
        if game.player.position.x == current_floor.vault.position.x and game.player.position.y == current_floor.vault.position.y:
            return True
            if game.player.has_key:
                return True
    return False

def clear_console():
    os.system('cls' if sys.platform == 'win32' else 'clear')

def main():
    game = Game(Vector(3,3), 3)
    running = True
    while running:
        clear_console()
        running = game_loop(game)
    
if __name__ == "__main__":
    main()