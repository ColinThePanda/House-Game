# item.py
from typing import List, Optional
from effect import Effect

class Item:
    def __init__(self, cost: int, name: str, description: str, effects: List[Effect] = None):
        self.cost: int = cost
        self.name: str = name
        self.description: str = description
        self.effects: List[Effect] = effects or []
        self.is_active: bool = True  # Whether the item's effects are currently active
    
    def apply_effects(self, target) -> None:
        """Apply all effects of this item to the target."""
        if self.is_active:
            for effect in self.effects:
                effect.apply(target)
    
    def remove_effects(self, target) -> None:
        """Remove all effects of this item from the target."""
        for effect in self.effects:
            effect.remove(target)
    
    def toggle_active(self) -> bool:
        """Toggle whether the item is active. Returns new state."""
        self.is_active = not self.is_active
        return self.is_active
    
    def get_full_description(self) -> str:
        """Get full description including effects."""
        base_desc = self.description
        effects_desc = []
        
        for effect in self.effects:
            effects_desc.append(f"• {effect.name}: {effect.description}")
        
        if effects_desc:
            return f"{base_desc}\n\nEffects:\n" + "\n".join(effects_desc)
        return base_desc