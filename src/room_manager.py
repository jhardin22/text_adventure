"""
Manages loading, instantiation, and access to all game rooms.
"""
import json
from pathlib import Path
from typing import Dict, Optional, Any

from .room import Room, HubRoom, StoryRoom
from .game_state import GameState

class RoomManager:
    """Loads and manages all Room objects for the game."""

    def __init__(self, rooms_data_path: str):
        """
        Initializes the RoomManager by loading room data from a file.
        """
        self.rooms: Dict[str, Room] = {}
        self._load_and_create_rooms(Path(rooms_data_path))

    def _load_and_create_rooms(self, path: Path):
        """Loads room data and creates corresponding Room objects."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                all_rooms_data = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Rooms data file not found at '{path}'. Cannot load rooms.")
            return

        for room_id, data in all_rooms_data.items():
            data['room_id'] = room_id  # Ensure the room knows its own ID
            room_type = data.get("type")
            
            if room_type == "hub":
                self.rooms[room_id] = HubRoom(data)
            elif room_type == "story":
                self.rooms[room_id] = StoryRoom(data)
            else:
                print(f"Warning: Unknown room type '{room_type}' for room '{room_id}'. Skipping.")

    def get_room(self, room_id: str) -> Optional[Room]:
        """Retrieves a full Room object by its ID."""
        return self.rooms.get(room_id)

    def get_exits_for_room(self, room_id: str) -> Dict[str, Any]:
        """Gets the exits dictionary for a given room from its object."""
        room = self.get_room(room_id)
        if room:
            return room.exits
        return {}

    def get_room_description(self, room_id: str, game_state: GameState) -> str:
        """Gets the descriptive text by calling the look() method on the Room object."""
        room = self.get_room(room_id)
        if room:
            return room.look(game_state)
        return "You find yourself in a void. Something is terribly wrong."