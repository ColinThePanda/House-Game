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
    
    def buy_item(self, item, debug=False):
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
    
    def clear_owned_items(self):
        self.data.items.clear()
        self.data_manager.save_data(self.data)

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
