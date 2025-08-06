from typing import Set, Dict, Any

class GameState:
    """
    Manages the player's progress and state within the game.
    This object is what will be saved and loaded.
    """
    def __init__(self):
        """Initializes a new game state."""
        self.current_room_id: str = "hub"
        self.inventory_ids: Set[str] = set()
        self.completed_doors: Set[str] = set()
        self.game_flags: Dict[str, Any] = {}
        
    def set_flag(self, flag_name: str, value: Any) -> None:
        """Sets a game flag to a specific value. (e.g., 'dog_has_spoken' = True)"""
        self.game_flags[flag_name] = value
        
    def get_flag(self, flag_name: str) -> Any:
        """Gets the value of a game flag, returns None if it doesn't exist."""
        return self.game_flags.get(flag_name)
    
    def add_item(self, item_id: str) -> None:
        """Adds an item's ID to the game state"""
        self.inventory_ids.add(item_id)
    
    def has_item(self, item_id: str) -> bool:
        """Checks if the player has a specific item by its ID"""
        return item_id in self.inventory_ids
    
    def complete_door(self, door_id: str) -> None:
        """Marks a door as completed by adding its ID to the set"""
        self.completed_doors.add(door_id)
        
    def is_door_completed(self, door_id: str) -> bool:
        """Checks if a door has been completed"""
        return door_id in self.completed_doors