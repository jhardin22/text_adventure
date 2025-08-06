"""
Core game logic for the text adventure.
"""

from typing import Dict, Any, Optional, List
import json
import os
from pathlib import Path

from src.inventory import Inventory, Item
from src.room import Room, HubRoom
from src.command_parser import CommandParser
from src.game_state import GameState

class TextAdventure:
    """Main game class that manages the overall game state and flow."""
    
    def __init__(self) -> None:
        """Initialize the game with configuration and starting state."""
        self.config: Dict[str, Any] = self._load_config()
        self.running: bool = False
                
        self.state = GameState()
        
        self.items: Dict[str, Item] = self._load_items()
        self.inventory = Inventory(self.items)
        self.rooms: Dict[str, Room] = self._load_rooms()
        
        self._sync_state()
        
        self.current_room: Room = self.rooms[self.state.current_room_id]
        self.parser = CommandParser()
    
    def _load_items(self) -> Dict[str, Item]:
        """Load all item data from the items.json file."""
        items_path = Path(self.config["file_paths"]["items_data"])
        all_items: Dict[str, Item] = {}
        try:
            with open(items_path, 'r', encoding='utf-8') as f:
                items_data = json.load(f)
                for item_id, data in items_data.items():
                    all_items[item_id] = Item(
                        item_id=item_id,
                        name=data.get("name", "Unknown Item"),
                        description=data.get("description", "No description available."),
                        flavor_text=data.get("flavor_text", "")
                    )
    
        except FileNotFoundError:
            print(f"Fatal Error: Item data file not found at {items_path}")
        except json.JSONDecodeError:
            print(f"Fatal Error: Failed to parse item data file at {items_path}")
        return all_items 
            
    def _load_config(self) -> Dict[str, Any]:
        """Load game configuration from config.json."""
        config_path = Path("data/config.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {config_path}")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if config file is missing."""
        return {
            "file_paths": {
                "rooms_data": "data/rooms.json",
                "items_data": "data/items.json",
                "save_directory": "saves/"
            },
            "display": {
                "line_width": 80,
                "separator": "=" * 50,
                "prompt": "> "
            },
            "game_settings": {
                "auto_save": True,
                "debug_mode": False,
                "max_save_slots": 5
            }
        }
        
    def _load_rooms(self) -> Dict[str, Room]:
        """
        Load all room data from rooms.json
        """
        rooms_path = Path(self.config["file_paths"]["rooms_data"])
        rooms: Dict[str, Room] = {}
        try:
            with open(rooms_path, 'r', encoding='utf-8') as f:
                rooms_data = json.load(f)
                
                for room_id, room_data in rooms_data.items():
                    room_instance = None
                    if room_data.get("type") == "hub":
                        room_instance = HubRoom(room_data)
                    # elif room_data.get("type") == "blue":
                    #     rooms[room_id] = BlueRoom(room_data)
                    # elif room_data.get("type") == "red":
                    #     rooms[room_id] = RedRoom(room_data)
                    # elif room_data.get("type") == "black":
                    #     rooms[room_id] = BlackRoom(room_ data)
                    else:
                        print(f"Warning: Unknown room type for room_id: {room_id}")
                        continue # Skip to the next iteration of the loop
                        
                    # This part runs only if a room_instance was created
                    for item_id in room_data.get("items", []):
                        if item_id in self.items:
                            room_instance.add_item(self.items[item_id])
                    
                    rooms[room_id] = room_instance
        except FileNotFoundError:
            print(f"Fatal Error: Room data file not found at {rooms_path}")
            raise
        except json.JSONDecodeError:
            print(f"Fatal Error: Failed to parse room data file at {rooms_path}")
            raise

        if not rooms: 
            raise ValueError("No rooms were loaded, check the data file.") 
        
        return rooms
            
               
    def run(self) -> None:
        """Main game loop."""
        self.running = True
        self._show_introduction()
        
        while self.running:
            try:
                user_input = input(self.config["display"]["prompt"]).strip()
                if not user_input:
                    continue
                
                self._process_command(user_input)
                
            except EOFError:
                # Handle Ctrl+D gracefully
                self.running = False
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                self.running = False
    
    def _show_introduction(self) -> None:
        """Display the game introduction."""
        print("You find yourself in a mysterious place...")
        print("A fluffy dog lays on a rug, looking at you expectantly.")
        print()
        print("Type 'help' for a list of commands.")
        print("Type 'quit' to exit the game.")
        print()
        self._look_around()
    
    def _process_command(self, user_input: str) -> None:
        """Process a player command using the command parser."""
        command, args = self.parser.parse(user_input)

        if command == "quit":
            print("Thanks for playing!")
            self.running = False
        elif command == "help":
            self._show_help(args)
        elif command == "look":
            self._handle_look(args)
        elif command == "go":
            self._handle_go(args)
        elif command == "inventory":
            self._handle_inventory()
        elif command == "take":
            self._handle_take(args)
        elif command is None:
            # The parser did not recognize the command
            print(f"I don't understand '{user_input}'. Type 'help' for available commands.")
        else:
            # A command was recognized but has no action yet
            print(f"The '{command}' command isn't implemented yet.")

    def _show_help(self, args: List[str]) -> None:
        """Display general help or help for a specific command."""
        if not args:
            # General help
            print("\nAvailable Commands:")
            print("Type 'help <command>' for more details on a specific command.")
            print("-" * 30)
            for command, details in self.parser.get_all_commands().items():
                print(f"  {command:<12} {details['description']}")
            print()
        else:
            # Specific command help
            command_name = args[0]
            details = self.parser.get_command_details(command_name)
            if details:
                aliases = ", ".join(details['aliases'])
                print(f"\n--- Help: {command_name} ---")
                print(f"Description: {details['description']}")
                print(f"Usage: {details['usage']}")
                if aliases:
                    print(f"Aliases: {aliases}")
                print()
            else:
                print(f"\nSorry, '{command_name}' is not a recognized command.")

    def _handle_look(self, args: List[str]) -> None:
        """Handles the 'look' command, for looking at the room or specific items."""
        if not args:
            # 'look' or 'look around'
            print(self.current_room.look())
        else:
            # 'look <target>'
            target_name = " ".join(args)
            # Check inventory first
            item_in_inventory = self.inventory.get_item_by_name(target_name)
            if item_in_inventory:
                print(item_in_inventory.description)
                if item_in_inventory.flavor_text:
                    print(item_in_inventory.flavor_text)
                return

            # Check room next
            item_in_room = self.current_room.get_item_by_name(target_name)
            if item_in_room:
                print(item_in_room.description)
                return
            
            print(f"You don't see any '{target_name}' here.")

    def _handle_go(self, args: List[str]) -> None:
        """Handles the 'go' command for movement."""
        if not args:
            print("Go where? (e.g., 'go north')")
            return
        
        direction = args[0]
        # This is where we'll add logic for locked doors later
        next_room_id = self.current_room.exits.get(direction)

        if next_room_id:
            self.state.current_room_id = next_room_id
            self.current_room = self.rooms[next_room_id]
            print(f"\nYou go {direction}...")
            self._handle_look([]) # Look around the new room
        else:
            print(f"You can't go {direction}.")

    def _handle_inventory(self) -> None:
        """Displays the player's inventory."""
        if self.inventory.is_empty():
            print("\nYour inventory is empty.")
        else:
            print("\nYou are carrying:")
            for item_name in self.inventory.list_items():
                print(f"  - {item_name}")
        print()

    def _handle_take(self, args: List[str]) -> None:
        """Handles the 'take' command for picking up items."""
        if not args:
            print("Take what?")
            return
        
        item_name = " ".join(args)
        item_to_take = self.current_room.get_item_by_name(item_name)

        if item_to_take:
            # Remove from room
            self.current_room.remove_item(item_to_take.item_id)
            # Add to inventory object
            self.inventory.add_item(item_to_take)
            # Add to game state
            self.state.add_item(item_to_take.item_id)
            print(f"You take the {item_to_take.name}.")
        else:
            print(f"You don't see any '{item_name}' here.")

    def _look_around(self) -> None:
        """A convenience wrapper for the look command."""
        self._handle_look([])