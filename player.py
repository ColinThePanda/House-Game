from vector import Vector
from typing import List
from item import Item

class Player():
    def __init__(self, position : Vector, items : List[Item]=[]):
        self.position : Vector = position
        self.can_move_up : bool = False
        self.can_move_down : bool = False
        self.has_key : bool = False
        self.can_teleport : bool = False  # Default teleport ability to False
        self.items : List[Item] = items
    
    def move(self, new_pos):
        self.position = new_pos
    
    def get_status_info(self):
        """Get a dictionary of player status information for UI display."""
        return {
            "position": f"({self.position.x + 1}, {self.position.y + 1})",
            "has_key": "Yes" if self.has_key else "No",
            "can_move_up": "Yes" if self.can_move_up else "No",
            "can_move_down": "Yes" if self.can_move_down else "No",
            "can_teleport": "Yes" if hasattr(self, 'can_teleport') and self.can_teleport else "No",
            "items": [item.name for item in self.items]
        }