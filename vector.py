class Vector():
    def __init__(self, x : int, y : int):
        self.x : int = x
        self.y : int = y
    
    def __add__(self):
        return self.x + self.y
    
    def __tuple__(self):
        return (self.x, self.y)