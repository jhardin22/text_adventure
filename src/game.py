"""
Core game logic for the text adventure.
"""

from typing import Dict, Any, Optional, List
import json
import os
from pathlib import Path

from src.inventory import Inventory, Item
from src.room import Room, HubRoom, StoryRoom
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
        Load all room data from individual .json files in the rooms directory.
        """
        rooms_dir = Path(self.config["file_paths"]["rooms_data"])
        rooms: Dict[str, Room] = {}
        
        if not rooms_dir.is_dir():
            print(f"Fatal Error: Room data directory not found at {rooms_dir}")
            raise FileNotFoundError

        for room_file in rooms_dir.glob('*.json'):
            try:
                with open(room_file, 'r', encoding='utf-8') as f:
                    room_data = json.load(f)
                    room_id = room_file.stem  # e.g., "hub.json" -> "hub"
                    
                    room_instance = None
                    room_type = room_data.get("type")
                    
                    if room_type == "hub":
                        room_instance = HubRoom(room_data)
                    elif room_type == "story":
                        room_data["room_id"] = room_id
                        room_instance = StoryRoom(room_data)
                    else:
                        print(f"Warning: Unknown room type for room_id: {room_id}")
                        continue
                        
                    # This part runs only if a room_instance was created
                    for item_id in room_data.get("items", []):
                        if item_id in self.items:
                            room_instance.add_item(self.items[item_id])
                    
                    rooms[room_id] = room_instance
            except json.JSONDecodeError:
                print(f"Fatal Error: Failed to parse room data file at {room_file}")
            except Exception as e:
                print(f"An unexpected error occurred loading {room_file}: {e}")

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
        elif command == "choose":
            self._handle_choose(args)
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
            print(self.current_room.look(self.state)) # MODIFIED: Pass the state
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
        exit_info = self.current_room.exits.get(direction)
        
        if not exit_info:
            print(f"You can't go {direction} from here.")
            return
        
        if isinstance(exit_info, dict):
            # This is a complex exit, potentially locked
            completion_flag = exit_info.get("completion_flag")
            if completion_flag and self.state.get_flag(completion_flag):
                print("That path is closed to you now.")
                return

            if exit_info.get("locked"):
                required_key = exit_info.get("key")
                if required_key and self.state.has_item(required_key):
                    # Player has key
                    print(exit_info.get("unlock_message", "The door seems to hum for a moment and slowly swings open."))
                    next_room_id = exit_info["destination"] #type: ignore
                else:
                    # Door is locked and player doesn't have key
                    message = exit_info.get("message", f"The door to the {direction} is locked.")
                    print(message)
                    return  # Important: return here to prevent movement
            else:
                # It's a complex exit but not locked
                next_room_id = exit_info["destination"] #type: ignore
        else:
            # It's a simple exit (just a string with the room ID)
            next_room_id = exit_info

        # Move the player to the new room
        self.state.current_room_id = next_room_id
        self.current_room = self.rooms[next_room_id]
        print(f"\nYou go {direction}...\n")
        self._handle_look([])  
        
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
            if item_to_take.flavor_text:
                print(f"{item_to_take.flavor_text}")
        else:
            print(f"You don't see any '{item_name}' here.")

    def _handle_choose(self, args: List[str]) -> None:
        """Handles the 'choose' command for story choices."""
        if not isinstance(self.current_room, StoryRoom):
            print("There are no choices to make here.")
            return

        current_node_data = self.current_room.get_current_node_data(self.state)
        if not current_node_data or "choices" not in current_node_data:
            print("There are no choices to make here.")
            return

        try:
            choice_num = int(args[0])
            choices = current_node_data["choices"]
            if not (1 <= choice_num <= len(choices)):
                raise ValueError
        except (ValueError, IndexError):
            print(f"That's not a valid choice. Please choose a number between 1 and {len(choices)}.")
            return

        selected_choice = choices[choice_num - 1]

        # --- NEW LOGIC: Check for a branch or a leaf ---
        next_node_id = selected_choice.get("next_node")
        if next_node_id:
            # This is a BRANCH. Update state and show the new choices.
            self.state.set_story_node(self.current_room.room_id, next_node_id)
            self._handle_look([]) # Re-display the room with the new choices
            return

        # This is a LEAF. Resolve the story as before.
        print(f"\n{selected_choice['outcome_text']}")

        reward_id = selected_choice.get("reward")
        if reward_id and reward_id in self.items:
            item = self.items[reward_id]
            self.inventory.add_item(item)
            self.state.add_item(item.item_id)
            print(f"You received: {item.name}")

        if self.current_room.completion_flag:
            self.state.set_flag(self.current_room.completion_flag, True)
            print("\nA feeling of finality settles over the memory.")

        hub_exit = self.current_room.exits.get("return")
        if hub_exit:
            self.state.current_room_id = hub_exit
            self.current_room = self.rooms[hub_exit]
            print("\nThe memory fades, and you find yourself back in the cavern.")
            self._handle_look([])

    def _look_around(self) -> None:
        """A convenience wrapper for the look command."""
        self._handle_look([])
        
    def _sync_state(self) -> None:
        """Sync the game state with the current room and inventory."""
        for item_id in self.state.inventory_ids:
            if item_id in self.items:
                self.inventory.add_item(self.items[item_id])
                
        for room in self.rooms.values():
            for item in list(room.items):
                if self.state.has_item(item.item_id):
                    room.remove_item(item.item_id)