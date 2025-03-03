from floor import Floor
from vector import Vector
from house import House

def main():
    house = House(Vector(5, 5), 4)
    house.print_tiles()

if __name__ == "__main__":
    main()