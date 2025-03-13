from items import Items
from item import Item
from typing import List, Union
from data_manager import DataManager
from rich.table import Table
from rich.console import Console
import keyboard
import time
import random
from typing import List, Dict, Any, Union, Optional
from rich.console import Console
from rich.table import Table
from ui import SelectionOption

class Shop:
    def __init__(self):
        print(self)
        self.data_manager = DataManager()
        self.data = self.data_manager.load_data()
        self.num_items = 4
        self.items: List[Item] = []
        self.populate_items()
    
    def populate_items(self):
        choices = [item.value for item in Items]
        items = []
        for i in range(self.num_items):
            item = random.choice(choices)
            items.append(item)
            choices.remove(item)
        self.items = items
    
    def buy_item(self, item: Item, debug: bool = False):
        if item in [i.value for i in Items]:  # Ensure we check against actual items
            if self.data.gold >= item.cost or debug:
                if not debug: self.data.gold -= item.cost 
                self.data.items.append(item)  # Use .append() to add an object
                self.data_manager.save_data(self.data)
                console = Console()
                console.print(f"Bought {item.name}")
                self.items.remove(self.items[self.items.index(item)])
    
    def clear_owned_items(self):
        self.data.items.clear()
        self.data_manager.save_data(self.data)

    def print_owned_items(self):
        console = Console()
        table = Table(title="Owned Items")

        table.add_column("Name", justify="center", style="bold", max_width=30)
        table.add_column("Cost", justify="center", style="bold", max_width=30)
        table.add_column("Description", justify="center", style="bold", max_width=30)
        
        for item in self.data.items:
            row = []
            row.append(item.name)
            row.append(str(item.cost))
            row.append(item.get_full_description())
            table.add_row(*row, style="bold")
        
        console.print(table)
    
    def print_options(self, highlighted: int):
        console = Console()
        table = Table(title="Available Items")

        table.add_column("Name", justify="center", style="bold", max_width=30)
        table.add_column("Cost", justify="center", style="bold", max_width=30)
        table.add_column("Description", justify="center", style="bold", max_width=50)
        
        for index, item in enumerate(self.items):
            row = []
            row.append(item.name)
            row.append(str(item.cost))
            row.append(item.get_full_description())
            
            if index == highlighted:
                table.add_row(*row, style="bold white on red")
            else:
                table.add_row(*row, style="bold")
        
        console.print(table)
    
    def get_input(self, index=0, interval=0.1, debug: bool = False) -> Union[bool, int]:
        console = Console()
        console.print(f"[yellow bold]Gold: {self.data.gold}[/yellow bold]")
        self.print_owned_items()
        self.print_options(index)
        time.sleep(interval)
        choice = keyboard.read_key()
        if choice == "up" or choice == "left":
            index -= 1
        if choice == "down" or choice == "right":
            index += 1
        if choice == "enter" or choice == "space":
            if index > len(self.items) - 1:
                index = len(self.items) - 1
            if index < 0:
                index = 0
            if len(self.items) <= 0:
                return True, index
            self.buy_item(self.items[index], debug=debug)
        if choice == "r":
            self.populate_items()
        if choice == "esc":
            return False, index
        if index < 0:
            index = len(self.items) + index
        if index > len(self.items) - 1:
            index = 0
        return True, index

    def get_shop_items_as_options(self):
        """Convert shop items to selection options."""
        options = []
        for item in self.items:
            options.append(SelectionOption(
                name=item.name,
                description=item.get_full_description(),
                value=item,
                additional_info={"cost": item.cost}
            ))
        return options
    
    def get_owned_items_table(self):
        """Create a rich table of owned items."""
        table = Table(title="Owned Items")
        table.add_column("Name", justify="center", style="bold", max_width=30)
        table.add_column("Description", justify="center", style="bold", max_width=50)
        
        for item in self.data.items:
            table.add_row(item.name, item.get_full_description(), style="bold")
        
        return table
    
    def purchase_item(self, item, debug=False):
        """Purchase an item with improved feedback."""
        console = Console()
        
        if item in self.items:
            if self.data.gold >= item.cost or debug:
                if not debug:
                    self.data.gold -= item.cost
                
                self.data.items.append(item)
                self.items.remove(item)
                
                self.data_manager.save_data(self.data)
                console.print(f"[green bold]Successfully purchased {item.name}![/green bold]")
                return True
            else:
                console.print(f"[red bold]Not enough gold to purchase {item.name}.[/red bold]")
                return False
        else:
            console.print("[red bold]Item not available in the shop.[/red bold]")
            return False
