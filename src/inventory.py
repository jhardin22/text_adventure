"""
Inventory management for the text adventure.
"""

from typing import List, Dict, Any, Optional


class Item:
    """Represents an item that can be collected and used."""
    
    def __init__(self, item_id: str, name: str, description: str, 
                 flavor_text: str = "", usable: bool = True) -> None:
        """Initialize an item with its properties."""
        self.item_id: str = item_id
        self.name: str = name
        self.description: str = description
        self.flavor_text: str = flavor_text
        self.usable: bool = usable

    @classmethod
    def from_dict(cls, item_id: str, data: Dict[str, Any]) -> 'Item':
        """Create an Item from dictionary data (for loading from JSON)."""
        return cls(
            item_id=item_id,
            name=data.get('name', 'Unknown Item'),
            description=data.get('description', 'No description available.'),
            flavor_text=data.get('flavor_text', ''),
            usable=data.get('usable', True)
        )

    def examine(self) -> str:
        """Return detailed examination text for the item."""
        text = f"**{self.name}**\n\n{self.description}"
        if self.flavor_text:
            text += f"\n\n*{self.flavor_text}*"
        return text


class Inventory:
    """Manages the player's inventory of items."""
    
    def __init__(self, all_items_data: Dict[str, Any], max_items: int = 10):
        """
        Initialize the inventory.

        Args:
            all_items_data: A dictionary of all possible items, loaded from JSON.
            max_items: The maximum number of items the player can hold.
        """
        self._all_items_data = all_items_data
        self.items: List[Item] = []
        self.max_items = max_items

    def add_item(self, item_id: str) -> bool:
        """Adds an item to the inventory by its ID. Returns True on success."""
        if self.is_full():
            print("Your inventory is full.")
            return False
        
        if self.has_item(item_id):
            print("You already have that item.")
            return False

        item_data = self._all_items_data.get(item_id)
        if not item_data:
            print(f"Error: No item data found for ID '{item_id}'.")
            return False
            
        new_item = Item.from_dict(item_id, item_data)
        self.items.append(new_item)
        return True

    def has_item(self, item_id: str) -> bool:
        """Checks if an item with the given ID is in the inventory."""
        return any(item.item_id == item_id for item in self.items)

    def get_item_by_name(self, name: str) -> Optional[Item]:
        """Finds an item in the inventory by its name (case-insensitive)."""
        search_name = name.lower()
        for item in self.items:
            if item.name.lower() == search_name:
                return item
        return None

    def is_empty(self) -> bool:
        """Returns True if the inventory has no items."""
        return not self.items

    def is_full(self) -> bool:
        """Returns True if the inventory is at maximum capacity."""
        return len(self.items) >= self.max_items

    def get_item_ids(self) -> List[str]:
        """Returns a list of all item IDs currently in the inventory."""
        return [item.item_id for item in self.items]