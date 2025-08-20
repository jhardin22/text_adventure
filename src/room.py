"""
Room management for the text adventure.
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from .inventory import Item
from .game_state import GameState  # Import GameState for managing game state

class Room(ABC):
    """Abstract base class for all rooms in the game."""
    
    def __init__(self, room_id: str, name: str, description: str) -> None:
        """Initialize a room with basic properties."""
        self.room_id: str = room_id
        self.name: str = name
        self.description: str = description
        self.items: List[Item] = []
        # This now correctly hints that each exit is a dictionary itself.
        self.exits: Dict[str, Dict[str, Any]] = {}
        self.visited: bool = False
    
    @abstractmethod
    def enter(self, game_state: 'GameState') -> str: # MODIFIED: Expects GameState
        """Called when player enters this room."""
        pass
    
    @abstractmethod
    def look(self, game_state: 'GameState') -> str:
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
    
    def enter(self, game_state: 'GameState') -> str: # MODIFIED: Parameter name
        """Handle entering the hub room."""
        self.visited = True
        return self.look(game_state) # MODIFIED: Pass the state
    
    def look(self, game_state: 'GameState') -> str:
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
    """A generic room for story segments that present choices."""
    def __init__(self, data: Dict[str, Any]) -> None:
        room_id = data.get("room_id")
        if not room_id:
            raise ValueError(f"StoryRoom created with invalid data. Missing 'room_id'. Data: {data}")

        super().__init__(
            room_id=room_id, # Now guaranteed to be a non-empty string
            name=data.get("name", "A Mysterious Place"),
            description=data.get("description", "You're in a room.")
        )
        self.exits = data.get("exits", {})
        self.story_nodes = data.get("story_nodes", {})
        self.completion_flag = data.get("completion_flag")
        
    def enter(self, game_state: 'GameState') -> str: # MODIFIED: Parameter name
        """Handle entering the story room."""
        self.visited = True
        # When entering a story room, we should show the current story node
        return self.look(game_state) # MODIFIED: Pass the state

    def get_current_node_data(self, game_state: 'GameState') -> Optional[Dict[str, Any]]:
        """Gets the data for the current story node based on game state."""
        current_node_id = game_state.get_story_node(self.room_id)
        return self.story_nodes.get(current_node_id)

    def look(self, game_state: 'GameState') -> str: # MODIFIED: Now uses GameState
        """Returns the description of the room and its current choices."""
        description = [self.description]
        if self.items:
            item_names = [item.name for item in self.items]
            description.append(f"You can see: {', '.join(item_names)}.")
            
        current_node = self.get_current_node_data(game_state)
        if current_node:
            prompt = current_node.get("prompt")
            choices = current_node.get("choices")
            if prompt and choices:
                description.append(f"\n{prompt}")
                for i, choice in enumerate(choices, 1):
                    description.append(f" {i}. {choice['text']}")
                description.append("\n(Type 'choose <number>' to make a selection)")
        return "\n".join(description)
