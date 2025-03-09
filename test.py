from player import Player
from vector import Vector

player = Player(Vector(1,1))

"""
    results = []
    for floor in range(10):
        for x in range(9):
                for y in range(9):
                    results.append({"x" : x+2, "y": y+2, "floors": floor+1, "result": calculate_gold(Game(Vector(x+2, y+2), floor+1))}) #Game(Vector(x+2, y+2), floor+1))f"X: {x+2}, Y: {y+2}, FLOORS: {floor+1}, RESULT: {calculate_gold(Game(Vector(x+2, y+2), floor+1))}")
    
    for item in results:
        print(f"X: {item['x']}, Y: {item['y']}, FLOORS: {item['floors']}, RESULT: {item['result']}")
"""