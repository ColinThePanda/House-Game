from vector import Vector
from data import SaveData
from data_manager import DataManager

class Player():
    def __init__(self, position : Vector, save_data : SaveData):
        self.position : Vector = position
        self.can_move_up : bool = False
        self.can_move_down : bool = False
        self.has_key : bool = False
        self.data : SaveData = save_data
    
    def move(self, new_pos):
        self.position = new_pos
