# items.py
from enum import Enum
from item import Item
from effect import PlayerEffect, GameEffect, EffectType
from player import Player

# Define effect functions at module level so they can be pickled
def key_sensor_effect(game):
    # Implementation to mark key tile as found
    for floor in game.house.floors:
        if floor.key:
            # Find tile by position and mark as found
            for tile in floor.tiles:
                if tile.position == floor.key.position:
                    tile.found = True

def teleport_ability(player: Player):
    # This attribute would be checked in the game loop
    # to add teleportation as a movement option
    player.can_teleport = True

class RevealerItem(Item):
    def __init__(self):
        reveal_effect = GameEffect(
            name="Revealer", 
            description="Reveals diagonal tiles",
            reveal_modifier=1
        )
        super().__init__(
            cost=100, 
            name="Revealer", 
            description="A magical lens that reveals more of your surroundings",
            effects=[reveal_effect]
        )

class GoldFinderItem(Item):
    def __init__(self):
        gold_effect = GameEffect(
            name="Gold Finder", 
            description="Increases gold rewards by 25%",
            gold_multiplier=1.25
        )
        super().__init__(
            cost=200, 
            name="Gold Finder", 
            description="A lucky charm that attracts more gold",
            effects=[gold_effect]
        )

class KeySensorItem(Item):
    def __init__(self):
        key_effect = GameEffect(
            name="Key Sensor", 
            description="Reveals the location of the key",
            custom_effect=key_sensor_effect  # Use the function defined at module level
        )
        super().__init__(
            cost=300, 
            name="Key Sensor", 
            description="A device that detects the key's location",
            effects=[key_effect]
        )

class TeleporterItem(Item):
    def __init__(self):
        teleport_effect = PlayerEffect(
            name="Teleporter", 
            description="Allows teleportation between discovered floors",
            custom_effect=teleport_ability  # Use the function defined at module level
        )
        super().__init__(
            cost=400, 
            name="Teleporter", 
            description="A device allowing instant travel between floors one has already visited",
            effects=[teleport_effect]
        )

# Define enum for easy access
class Items(Enum):
    REVEALER = RevealerItem()
    GOLD_FINDER = GoldFinderItem()
    KEY_SENSOR = KeySensorItem()
    TELEPORTER = TeleporterItem()