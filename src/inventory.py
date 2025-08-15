"""
Inventory management for the text adventure.
"""

from typing import List, Dict, Any, Optional


class Item:
    """Represents an item that can be collected and used."""
    
    def __init__(self, item_id: str, name: str, description: str, 
                 flavor_text: str = "") -> None:
        """Initialize an item with its properties."""
        self.item_id: str = item_id
        self.name: str = name
        self.description: str = description
        self.flavor_text: str = flavor_text
        self.usable: bool = True


class Inventory:
    """Manages the player's inventory of items."""
    
    def __init__(self, all_items: Dict[str, Item]) -> None:
        """Initialize an empty inventory."""
        self.items: List[Item] = []
        self.max_items: int = 10  # Reasonable limit
        self._item_definitions = all_items # Keep a reference to all possible items

    def add_item(self, item: Item) -> bool:
        """Add an item to the inventory."""
        if len(self.items) >= self.max_items:
            return False
        
        # Check if item already exists
        if any(existing.item_id == item.item_id for existing in self.items):
            return False
        
        self.items.append(item)
        return True
    
    def remove_item(self, item_id: str) -> Optional[Item]:
        """Remove and return an item from inventory."""
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                return item
        return None
    
    def has_item(self, item_id: str) -> bool:
        """Check if inventory contains a specific item."""
        return any(item.item_id == item_id for item in self.items)
    
    def get_item(self, item_id: str) -> Optional[Item]:
        """Get an item from inventory without removing it."""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None
    
    def get_item_by_name(self, name: str) -> Optional[Item]:
        """Finds an item in the inventory by its name (case-insensitive)."""
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

    def list_items(self) -> List[str]:
        """Return a list of item names in inventory."""
        return [item.name for item in self.items]
    
    def is_empty(self) -> bool:
        """Check if inventory is empty."""
        return len(self.items) == 0
    
    def count(self) -> int:
        """Return the number of items in inventory."""
        return len(self.items)