from main import calculate_gold
from game import Game
from vector import Vector

print(calculate_gold(Game(Vector(3, 3), floors=3)))
print(calculate_gold(Game(Vector(5, 5), 3)))
print(calculate_gold(Game(Vector(9, 9), 5)))