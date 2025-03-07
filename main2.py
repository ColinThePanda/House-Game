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
import keyboard

def game_loop(game : Game):
    console = Console()

    options = game.get_options()

    # Wait for a valid key press before continuing
    valid_keys = list(get_option_keys().values())  
    
    interval = 0.15
    is_valid_move = False
    while not is_valid_move:
        move = None
        while move not in valid_keys:
            move = keyboard.read_key()  # Waits for a key press
            if move in valid_keys:
                break  # Valid key detected, continue execution
        if move == "esc":
            return False
        elif move == "up":
            position = Vector(game.player.position.x, game.player.position.y + 1)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            else:
                is_valid_move = False
        elif move == "down":
            position = Vector(game.player.position.x, game.player.position.y - 1)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            else:
                is_valid_move = False
        elif move == "left":
            position = Vector(game.player.position.x - 1, game.player.position.y)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            else:
                is_valid_move = False
        elif move == "right":
            position = Vector(game.player.position.x + 1, game.player.position.y)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            else:
                is_valid_move = False
        elif move == "space":  # Handle both "move up" and "move down"
            if "move up" in options:
                is_valid_move = True
                interval = 0.5
                game.move_floor(game.current_floor + 1)
            elif "move down" in options:
                is_valid_move = True
                interval = 0.5
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
        time.sleep(5)
        return False

    return True, interval

def check_win(game : Game):
    current_floor : Floor = game.house.floors[game.current_floor - 1]
    if current_floor.vault:
        if game.player.position.x == current_floor.vault.position.x and game.player.position.y == current_floor.vault.position.y:
            if game.player.has_key:
                return True
    return False

def clear_console():
    os.system('cls' if sys.platform == 'win32' else 'clear')

def print_choices(options : list):
    console = Console()
    option_colors = get_option_colors()
    option_keys = get_option_keys()
    
    # Create colored text for each option
    colored_options = []
    for option in options:
        color = option_colors.get(option, "white")
        key = option_keys.get(option, " ")
        colored_options.append(f"[{color}]{option} : {key}[/{color}]")
    
    # Display the prompt with colored options
    console.print(f"What do you want to do? ({', '.join(colored_options)})")

def get_option_colors():
    return {
        "up": "blue",
        "down": "blue",
        "left": "blue",
        "right": "blue",
        "move up": "green",
        "move down": "red",
        "exit": "yellow"
    }

def get_option_keys():
    return {
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
        "move up": "space",
        "move down": "space",
        "exit": "esc"
    }

def get_game():
    size = int(input("1. Small House\n2. Medium House\n3. Large House\n4. Extra Large\n5. Custom\n"))
    if size != 5:
        diagonals = bool(int(input("Should diagonals be revealed? (1. yes, 0. no) ")))
    if size == 1:
        game = Game(Vector(3, 3), 3, diagonals)
    elif size == 2:
        game = Game(Vector(5, 5), 3, diagonals)
    elif size == 3:
        game = Game(Vector(7, 7), 3, diagonals)
    elif size == 4:
        game = Game(Vector(9, 9), 5, diagonals)
    elif size == 5:
        game = Game(Vector(int(input("How big should each floor be on the x axis? ")), int(input("How big should each floor be on the y axis? "))), int(input("How many floors should the house have? "),) , bool(int(input("Should diagonals be revealed? (1. yes, 0. no) "))))
    else:
        print("Invalid input")
        print("Picking Medium House")
        game = Game(Vector(5, 5), 3, diagonals)
        time.sleep(3)
    return game

def main():
    game = get_game()
    running = True
    interval = 0.0
    while running :
        clear_console()
        game.print_floor(game.current_floor)
        print_choices(game.get_options())
        time.sleep(interval)
        running, interval = game_loop(game)

    
if __name__ == "__main__":
    main()
