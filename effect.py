# effect.py
from enum import Enum
from typing import Any, Dict, Callable, TYPE_CHECKING

# Type checking imports that don't cause circular imports at runtime
if TYPE_CHECKING:
    from player import Player
    from game import Game

class EffectType(Enum):
    PLAYER = 0  # Effects that modify player attributes
    GAME = 1    # Effects that modify game mechanics
    FLOOR = 2   # Effects that modify floor generation
    COMBAT = 3  # For future combat system

class Effect:
    def __init__(self, effect_type: EffectType, name: str, description: str):
        self.type = effect_type
        self.name = name
        self.description = description
    
    def apply(self, target: Any) -> None:
        """
        Base method to apply the effect to a target.
        To be overridden by subclasses.
        """
        pass
    
    def remove(self, target: Any) -> None:
        """
        Base method to remove the effect from a target.
        To be overridden by subclasses.
        """
        pass


class PlayerEffect(Effect):
    def __init__(self, name: str, description: str, 
                 attribute_modifiers: Dict[str, Any] = None,
                 custom_effect: Callable[["Player"], None] = None):
        super().__init__(EffectType.PLAYER, name, description)
        self.attribute_modifiers = attribute_modifiers or {}
        self.custom_effect = custom_effect
    
    def apply(self, player: "Player") -> None:
        # Apply attribute modifiers
        for attr, value in self.attribute_modifiers.items():
            if hasattr(player, attr):
                original_value = getattr(player, attr)
                # Store original value to restore later
                if not hasattr(player, '_original_values'):
                    player._original_values = {}
                if attr not in player._original_values:
                    player._original_values[attr] = original_value
                
                # Apply modifier (could be more complex based on type)
                if isinstance(original_value, bool):
                    setattr(player, attr, value)
                elif isinstance(original_value, (int, float)):
                    setattr(player, attr, original_value + value)
                # Add more types as needed
        
        # Apply custom effect if provided
        if self.custom_effect:
            self.custom_effect(player)
    
    def remove(self, player: "Player") -> None:
        # Restore original values
        if hasattr(player, '_original_values'):
            for attr, value in self.attribute_modifiers.items():
                if attr in player._original_values:
                    setattr(player, attr, player._original_values[attr])
                    del player._original_values[attr]


class GameEffect(Effect):
    def __init__(self, name: str, description: str,
                 reveal_modifier: int = 0,
                 gold_multiplier: float = 1.0,
                 custom_effect: Callable[["Game"], None] = None):
        super().__init__(EffectType.GAME, name, description)
        self.reveal_modifier = reveal_modifier
        self.gold_multiplier = gold_multiplier
        self.custom_effect = custom_effect
    
    def apply(self, game: "Game") -> None:
        # Store original values
        if not hasattr(game, '_original_values'):
            game._original_values = {
                'reveal_diagonals': game.reveal_diagonals,
                'gold_multiplier': 1.0  # Assume default is 1.0
            }
        
        # Apply modifiers
        if self.reveal_modifier > 0:
            game.reveal_diagonals = True
        
        # Apply custom effect for more complex behaviors
        if hasattr(game, 'gold_multiplier'):
            game.gold_multiplier *= self.gold_multiplier
        else:
            game.gold_multiplier = self.gold_multiplier
            
        if self.custom_effect:
            self.custom_effect(game)
    
    def remove(self, game: "Game") -> None:
        if hasattr(game, '_original_values'):
            game.reveal_diagonals = game._original_values['reveal_diagonals']
            game.gold_multiplier = game._original_values['gold_multiplier']