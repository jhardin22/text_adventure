"""
Room management for the text adventure.
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from .inventory import Item

class Room(ABC):
    """Abstract base class for all rooms in the game."""
    
    def __init__(self, room_id: str, name: str, description: str) -> None:
        """Initialize a room with basic properties."""
        self.room_id: str = room_id
        self.name: str = name
        self.description: str = description
        self.items: List[Item] = []
        self.exits: Dict[str, str] = {}
        self.visited: bool = False
    
    @abstractmethod
    def enter(self, player_state: Dict[str, Any]) -> str:
        """Called when player enters this room."""
        pass
    
    @abstractmethod
    def look(self) -> str:
        """Return the room's description when player looks around."""
        pass
    
    def add_item(self, item: Item) -> None:
        """Add an item to this room."""
        if not any(i.item_id == item.item_id for i in self.items):
            self.items.append(item)

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from this room."""
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                return True
        return False

    def get_item_by_name(self, name: str) -> Optional[Item]:
        """Finds an item in the room by its name (case-insensitive)."""
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

class HubRoom(Room):
    """The central hub room with the talking dog and three doors."""
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(
            room_id="hub",
            name=data.get("name", "The Hub"),
            description=data.get("description", "A warm, welcoming space with a friendly dog and three mysterious doors.")
        )
        self.details = data.get("details", {})
        self.exits = data.get("exits", {})
    
    def enter(self, player_state: Dict[str, Any]) -> str:
        """Handle entering the hub room."""
        self.visited = True
        return self.look()
    
    def look(self) -> str:
        """Return the hub room description."""
        description = [
            self.description, # Use the description loaded from JSON
            self.details.get("dog", "A friendly dog is here."),
            self.details.get("doors", "You see three doors."),
        ]
        
        if self.items:
            item_names = [item.name for item in self.items]
            description.append(f"On the floor, you see: {', '.join(item_names)}.")
        
        return "\n".join(description)
    
class StoryRoom(Room):
    """A generic room for story segements."""
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(
            room_id=data.get("room_id"),
            name=data.get("name", "A Mysterious Place"),
            description=data.get("description", "You're in a room.")
        )
        self.exits = data.get("exits", {})
        
    def enter(self, player_state: Dict[str, Any]) -> str:
        self.visited = True
        return self.look()
    
    def look(self) -> str:
        description = [self.description]
        if self.items:
            item_names = [item.name for item in self.items]
            description.append(f"You can see: {', '.join(item_names)}.")
        return "\n".join(description)
        