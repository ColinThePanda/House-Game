from floor import Floor
from vector import Vector
from house import House
from game import Game
from tile import Tile, TileType

def main():
    game = Game(Vector(3,3), 3)
    game.print_floor(1)
    print(Vector(game.player.position.x, game.player.position.y).xy)
    move : str = input("where move(up, down, left, right)?")
    if move == "up":
        game.move_player(Vector(game.player.position.x, game.player.position.y + 1))
    if move == "down":
        game.move_player(Vector(game.player.position.x, game.player.position.y))
    if move == "left":
        game.move_player(Vector(game.player.position.x - 1, game.player.position.y))
    if move == "right":
        game.move_player(Vector(game.player.position.x + 1, game.player.position.y + 1))
    print(game.player.position.xy)
    game.print_floor(1)
if __name__ == "__main__":
    main()