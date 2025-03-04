from vector import Vector

class Player():
    def __init__(self, position : Vector):
        self.position : Vector = position
        self.can_move_up : bool = False
        self.can_move_down : bool = False
    
    def move(self, new_pos):
        self.position = new_pos
