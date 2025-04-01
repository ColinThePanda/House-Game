# game_utils.py - Reusable input, teleporting, and selection UI functions
import os
import sys
import time
import keyboard
from rich.console import Console
from rich.table import Table
from rich.text import Text
from vector import Vector
from typing import List, Dict, Any, Callable, Optional, Tuple, Union
from game import Game
from ascii_art import ascii_shop, ascii_main, ascii_win

def clear_console():
    """Clear the console screen based on the operating system."""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def get_movement_options(game):
    """Get available movement options based on player position and game state."""
    options = []
    current_floor = game.house.floors[game.current_floor - 1]
    
    # Cardinal directions
    if game.player.position.y < current_floor.size.y - 1:
        options.append("up")
    if game.player.position.y > 0:
        options.append("down")
    if game.player.position.x > 0:
        options.append("left")
    if game.player.position.x < current_floor.size.x - 1:
        options.append("right")
    
    # Floor movement
    if game.player.can_move_up:
        options.append("move up")
    if game.player.can_move_down:
        options.append("move down")
    
    # Teleport option if player has the ability
    if hasattr(game.player, 'can_teleport') and game.player.can_teleport:
        options.append("teleport")
    
    options.append("exit")
    return options

def get_option_colors():
    """Define colors for different movement options."""
    return {
        "up": "blue",
        "down": "blue",
        "left": "blue",
        "right": "blue",
        "move up": "green",
        "move down": "red",
        "teleport": "magenta",
        "exit": "yellow"
    }

def get_option_keys():
    """Define keyboard keys for different movement options."""
    return {
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
        "move up": "space",
        "move down": "space",
        "teleport": "t",
        "exit": "esc"
    }

def print_choices(options):
    """Display available movement options with colors and key bindings."""
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


# Generic Selection Interface
class SelectionOption:
    """A single option in a selection interface."""
    def __init__(self, 
                 name: str, 
                 description: str = "", 
                 value: Any = None, 
                 additional_info: Dict[str, Any] = None):
        self.name = name
        self.description = description
        self.value = value if value is not None else name
        self.additional_info = additional_info or {}
    
    def __str__(self):
        return self.name

def show_selection_interface(
    title: str,
    options: List[SelectionOption],
    initial_index: int = 0,
    columns: List[Tuple[str, str]] = None,
    header_text: str = None,
    footer_text: str = None,
    highlight_style: str = "bold white on blue",
    normal_style: str = "bold",
    cancel_allowed: bool = True,
    display_callback: Callable = None,
    action_callback: Callable = None
) -> Optional[Any]:
    """
    Generic selection interface for picking from a list of options.
    
    Args:
        title: Title of the selection interface
        options: List of SelectionOption objects
        initial_index: Starting selection index
        columns: List of (name, key) tuples defining table columns
                 Default shows just the name column
        header_text: Optional text to display above the selection table
        footer_text: Optional text to display below the selection table
        highlight_style: Rich style string for the highlighted option
        normal_style: Rich style string for normal options
        cancel_allowed: Whether ESC can be used to cancel
        display_callback: Optional function(console, selected_index, options) to customize display
        action_callback: Optional function(selected_option, index) called when an option is selected
    
    Returns:
        The value of the selected option or None if cancelled
    """
    if not options:
        return None
    
    # Default to showing just name column if not specified
    if columns is None:
        columns = [("Name", "name")]
    
    console = Console()
    selected_index = min(max(0, initial_index), len(options) - 1)
    
    running = True
    first_run = True
    
    while running:
        clear_console()
        
        # Display title and header
        console.print(title)
        if header_text:
            console.print(header_text)
        
        # If custom display is provided, use it
        if display_callback:
            display_callback(console, selected_index, options)
        else:
            # Create default table display
            table = Table(title="", show_header=True)
            
            # Add columns
            for col_name, _ in columns:
                table.add_column(col_name)
                
            # Add rows
            for i, option in enumerate(options):
                row = []
                for _, col_key in columns:
                    # Handle nested attributes with dot notation
                    if "." in col_key:
                        parts = col_key.split(".")
                        value = option
                        for part in parts:
                            if hasattr(value, part):
                                value = getattr(value, part)
                            elif isinstance(value, dict) and part in value:
                                value = value[part]
                            else:
                                value = "N/A"
                                break
                    else:
                        value = getattr(option, col_key) if hasattr(option, col_key) else "N/A"
                    
                    # Convert to string
                    row.append(str(value))
                
                # Apply highlighting to selected row
                style = highlight_style if i == selected_index else normal_style
                table.add_row(*row, style=style)
            
            console.print(table)
        
        # Display footer
        if footer_text:
            console.print(footer_text)
        
        # Display controls
        controls = ["[↑/↓] Navigate"]
        if cancel_allowed:
            controls.append("[Esc] Cancel")
        controls.append("[Space/Enter] Select")
        console.print(" | ".join(controls))

        time.sleep(0.2)

        # Wait for input
        key = keyboard.read_key()
        
        if key == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key in ["space", "enter"]:
            selected = options[selected_index]
            
            # Call action callback if provided
            if action_callback:
                action_result = action_callback(selected, selected_index)
                # If the callback returns a specific value, use it
                if action_result is not None:
                    return action_result
                
            # Otherwise return the option's value
            return selected.value
        elif key == "esc" and cancel_allowed:
            return None

        first_run = False
    
    return None

def handle_player_input(game, interval=0.15):
    """
    Handle player input for movement and actions.
    
    Args:
        game: The game instance
        interval: Time interval for animation/delay
    
    Returns:
        tuple: (is_game_running, animation_interval)
    """
    options = get_movement_options(game)
    valid_keys = list(get_option_keys().values())
    
    is_valid_move = False
    while not is_valid_move:
        move = None
        while move not in valid_keys:
            move = keyboard.read_key()  # Waits for a key press
            if move in valid_keys:
                break  # Valid key detected, continue execution

        if move == "esc":
            return False, interval  # Exit game
        
        # Handle directional movement
        elif move == "up":
            position = Vector(game.player.position.x, game.player.position.y + 1)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            
        elif move == "down":
            position = Vector(game.player.position.x, game.player.position.y - 1)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            
        elif move == "left":
            position = Vector(game.player.position.x - 1, game.player.position.y)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            
        elif move == "right":
            position = Vector(game.player.position.x + 1, game.player.position.y)
            if game.is_valid_move(position):
                is_valid_move = True
                game.move_player(position)
            
        # Handle floor movement
        elif move == "space":
            if "move up" in options:
                is_valid_move = True
                interval = 0.5
                game.move_floor(game.current_floor + 1)
            elif "move down" in options:
                is_valid_move = True
                interval = 0.5
                game.move_floor(game.current_floor - 1)
        
        # Handle teleportation
        elif move == "t" and "teleport" in options:
            target_floor = show_teleport_ui(game)
            if target_floor is not None:
                is_valid_move = True
                interval = 0.5
                game.move_floor(target_floor)
    
    return True, interval

def show_teleport_ui(game : Game):
    """
    Show teleportation floor selection UI using the generic selection interface.
    
    Args:
        game: The game instance
    
    Returns:
        int or None: The selected floor number or None if canceled
    """
    # Get accessible (discovered) floors
    floor_options = []
    
    for floor in game.house.floors:
        #if (hasattr(floor, 'discovered') and floor.discovered) or floor.index + 1 == game.current_floor + 1:
        name = f"Floor {floor.index + 1}"
        if floor.index + 1 == game.current_floor:
            name += " (current)"
        
        floor_options.append(SelectionOption(
            name=name,
            description=f"Floor {floor.index + 1}",
            value=floor.index + 1,  # Return 1-based floor number
            additional_info={"is_current": floor.index + 1 == game.current_floor}
        ))
    
    if not floor_options:
        console = Console()
        console.print("[bold red]No floors available for teleportation![/bold red]")
        time.sleep(1.5)
        return None
    
    # Find current floor in options
    initial_index = 0
    for i, option in enumerate(floor_options):
        if option.additional_info.get("is_current", False):
            initial_index = i
            break
    
    # Use generic selection interface
    return show_selection_interface(
        title="Select Floor to Teleport To",
        options=floor_options,
        initial_index=initial_index,
        header_text="Choose a floor to teleport to:\n",
        footer_text=None,
        columns=[("Floor", "name")],
        highlight_style="bold white on blue",
        normal_style="bold",
        cancel_allowed=True
    )

def handle_shop_interface(shop, debug=False):
    """
    Show shop interface using the generic selection interface.
    
    Args:
        shop: The shop instance
        debug: Enable debug mode (free items)
    
    Returns:
        bool: Whether the shop should continue running
    """
    # Custom header display function to show gold
    def display_header(console : Console, selected_index, options):
        console.print(f"[yellow bold]Gold: {shop.data.gold}[/yellow bold]")
        console.print("\n[bold]Owned Items:[/bold]")
        
        # Display owned items
        if shop.data.items:
            owned_table = Table(show_header=True)
            owned_table.add_column("Name")
            owned_table.add_column("Description")
            
            for owned_item in shop.data.items:
                owned_table.add_row(
                    owned_item.name,
                    owned_item.get_full_description()
                )
            console.print(owned_table)
        else:
            console.print("[italic]No items owned yet.[/italic]")
        
        console.print("\n[bold]Available Items:[/bold]")
    
    # Custom action to handle purchase using buy_item function
    def purchase_action(selected_option, index):
        item = selected_option.value
        
        # Use the buy_item function directly
        purchase_successful = shop.buy_item(item, debug)
        
        # If purchase was successful, no need to return anything - we'll refresh the interface
        if purchase_successful:
            time.sleep(1)
        else:
            # If purchase failed (not enough gold or item not available)
            time.sleep(1)
        
        # Return None to continue shopping
        return None
    
    # Additional footer text with controls
    footer_text = "[R] Refresh shop | [Esc] Exit shop"
    
    # Custom display function to handle case when shop is empty
    def custom_display(console, selected_index, options):
        display_header(console, selected_index, options)
        
        if not options:
            console.print("[italic]No items available in the shop.[/italic]")
            console.print("\nPress [R] to refresh the shop inventory or [Esc] to exit.")
            return
        
        # Display items table
        table = Table(show_header=True)
        table.add_column("Name")
        table.add_column("Cost")
        table.add_column("Description")
        
        for i, option in enumerate(options):
            item = option.value
            style = "bold white on blue" if i == selected_index else "bold"
            table.add_row(
                item.name,
                str(item.cost),
                item.get_full_description(),
                style=style
            )
        
        console.print(table)
    
    # Handle shop interface
    while True:
        # Convert shop items to selection options
        item_options = shop.get_shop_items_as_options()
        
        # Handle empty shop
        if not item_options:
            clear_console()
            console = Console()
            display_header(console, 0, [])
            console.print("[italic]No items available in the shop.[/italic]")
            console.print("\nPress [R] to refresh the shop inventory or [Esc] to exit.")
            
            key = keyboard.read_key()
            if key == "r":
                shop.populate_items()
                time.sleep(0.2)
                continue
            elif key == "esc":
                return False
            
            time.sleep(0.2)
            continue
        
        # Show selection interface
        result = show_selection_interface(
            title=ascii_shop,
            options=item_options,
            initial_index=0,
            header_text=None,  # We're using custom display
            footer_text=footer_text,
            columns=[("Name", "name"), ("Cost", "additional_info.cost"), ("Description", "description")],
            display_callback=custom_display,
            action_callback=purchase_action,
            cancel_allowed=True
        )
        
        # Handle special keys not handled by selection interface
        if result == "refresh":
            shop.populate_items()
        elif result == "exit" or result is None:
            return False
        
        # Check for empty shop after purchase
        if not shop.items:
            console = Console()
            console.print("[yellow]Shop is empty! Press [R] to refresh or [Esc] to exit.[/yellow]")
            
            # Wait for input
            while True:
                key = keyboard.read_key()
                if key == "r":
                    shop.populate_items()
                    break
                elif key == "esc":
                    return False
                time.sleep(0.2)

def run_game_interface(game):
    """
    Main game interface loop.
    
    Args:
        game: The game instance
        
    Returns:
        bool: True if game ended successfully, False otherwise
    """
    running = True
    interval = 0.0
    
    while running:
        clear_console()
        
        # Display current floor information
        current_floor = game.house.floors[game.current_floor - 1]
        print(f"Floor {game.current_floor} - Discovered: {current_floor.discovered}")
        
        # Display game map
        game.print_floor(game.current_floor)
        
        # Display available options
        options = get_movement_options(game)
        print_choices(options)
        
        # Process input after slight delay (for animation)
        time.sleep(interval)
        running, interval = handle_player_input(game)
        
        # Check win condition
        if check_win_condition(game):
            return True
    
    return False


def check_win_condition(game : Game):
    """
    Check if the player has won the game.
    
    Args:
        game: The game instance
        
    Returns:
        bool: True if player has won, False otherwise
    """
    current_floor = game.house.floors[game.current_floor - 1]
    
    # Check if player is on vault tile and has key
    if current_floor.vault:
        if (game.player.position.x == current_floor.vault.position.x and 
            game.player.position.y == current_floor.vault.position.y):
            if game.player.has_key:
                # Calculate gold reward
                from main import calculate_gold  # Import calculation function
                gold_earned = calculate_gold(game)
                game.data.gold += gold_earned
                game.save_data()
                display_win_screen(game, 5, gold_earned)
                return True
    
    return False


def display_win_screen(game : Game, seconds : int, gold_earned : int):
    """
    Display the win screen with ASCII art and rewards.
    
    Args:
        game: The game instance
    """
    clear_console()
    
    console = Console()

    # Display win ASCII art
    console.print(ascii_win)
    
    # Display game summary
    #game.print_floor(game.current_floor)
    
    console.print(f"[yellow bold]Gold earned: {gold_earned}[/yellow bold]")
    console.print(f"[yellow bold]Total gold: {game.data.gold}[/yellow bold]")
    
    console.print(f"Restarting in {seconds}")
    seconds -= 1
    if seconds >= 0:
        time.sleep(1)
        display_win_screen(game, seconds, gold_earned)


def game_setup_interface():
    """
    Interface for setting up a new game.
    
    Returns:
        Game: The configured game instance
    """
    console = Console()
    console.print("[bold]House Explorer Setup[/bold]\n")
    
    # House size options
    size_options = [
        SelectionOption(name="Small House (3x3)", description="3x3 grid, 3 floors", value=1),
        SelectionOption(name="Medium House (5x5)", description="5x5 grid, 3 floors", value=2),
        SelectionOption(name="Large House (7x7)", description="7x7 grid, 3 floors", value=3),
        SelectionOption(name="Extra Large (9x9)", description="9x9 grid, 5 floors", value=4),
        SelectionOption(name="Custom Size", description="Define your own dimensions", value=5)
    ]

    # Get house size selection
    size_choice = show_selection_interface(
        title="Select House Size",
        options=size_options,
        initial_index=1,  # Default to medium
        columns=[("Size", "name"), ("Details", "description")],
        header_text="Choose the size of the house to explore:",
        cancel_allowed=False
    )
    
    # Handle custom size
    if size_choice == 5:
        clear_console()
        console.print("[bold]Custom House Configuration[/bold]\n")
        
        # Get custom dimensions with validation
        while True:
            try:
                x_size = int(input("Enter floor width (x-axis size, 2-15): "))
                if 2 <= x_size <= 15:
                    break
                console.print("[red]Please enter a value between 2 and 15.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
        
        while True:
            try:
                y_size = int(input("Enter floor height (y-axis size, 2-15): "))
                if 2 <= y_size <= 15:
                    break
                console.print("[red]Please enter a value between 2 and 15.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
        
        while True:
            try:
                floors = int(input("Enter number of floors (1-10): "))
                if 1 <= floors <= 10:
                    break
                console.print("[red]Please enter a value between 1 and 10.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    # Create game based on selections
    from game import Game
    from vector import Vector
    
    if size_choice == 1:
        game = Game(Vector(3, 3), 3)
    elif size_choice == 2:
        game = Game(Vector(5, 5), 3)
    elif size_choice == 3:
        game = Game(Vector(7, 7), 3)
    elif size_choice == 4:
        game = Game(Vector(9, 9), 5)
    elif size_choice == 5:
        game = Game(Vector(x_size, y_size), floors)
    else:
        # Fallback to medium if something went wrong
        console.print("[yellow]Invalid selection, using Medium House.[/yellow]")
        game = Game(Vector(5, 5), 3)
        time.sleep(2)
    
    return game


def main_menu():
    """
    Main menu interface for the game.
    
    Returns:
        None
    """

    clear_console()
    console = Console()
    
    # Display title
    console.print(f"""{ascii_main}

[white]Press any key to play...[/white]

""")

    keyboard.read_key()