"""
Room management for the text adventure.
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod


class Room(ABC):
    """Abstract base class for all rooms in the game."""
    
    def __init__(self, room_id: str, name: str, description: str) -> None:
        """Initialize a room with basic properties."""
        self.room_id: str = room_id
        self.name: str = name
        self.description: str = description
        self.items: List[str] = []
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
    
    def add_item(self, item_id: str) -> None:
        """Add an item to this room."""
        if item_id not in self.items:
            self.items.append(item_id)
    
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from this room."""
        if item_id in self.items:
            self.items.remove(item_id)
            return True
        return False


class HubRoom(Room):
    """The central hub room with the talking dog and three doors."""
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(
            room_id="hub",
            name=data.get("name", "The Hub"),
            description=data.get("description", "A warm, welcoming space with a friendly dog and three mysterious doors.")
        )
        self.details = data.get("details", {})
    
    def enter(self, player_state: Dict[str, Any]) -> str:
        """Handle entering the hub room."""
        self.visited = True
        return self.look()
    
    def look(self) -> str:
        """Return the hub room description."""
        description = [
            "You are in a large cavern with rock walls.",
            self.details.get("doors", "Three ornate doors are evenly spaced around the room."),
            self.details.get("dog", "A large fluffy dog lays on the rug in the middle of the room.")
        ]
        
        if self.items:
            description.append(f"You can see: {', '.join(self.items)}")
        
        return "\n".join(description)