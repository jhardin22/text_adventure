"""
Core game logic for the text adventure.
"""

import os, json
from typing import Dict, Any, Optional, List
from pathlib import Path

from src.config_loader import ConfigLoader, ConfigurationError
from src.inventory import Inventory
from src.room_manager import RoomManager
from src.game_state import GameState

class TextAdventureGame:
    """Main game class that coordinates all game systems."""
    
    def __init__(self):
        """Initialize the game with configuration and core systems."""
        # Load configuration first
        try:
            self.config_loader = ConfigLoader()
            self.config = self.config_loader.load()
            print("Configuration loaded successfully.")
        except ConfigurationError as e:
            print(f"Configuration Error: {e}")
            if e.errors:
                for error in e.errors:
                    print(f"  - {error.path}: {error.message}")
            raise SystemExit("Cannot start game due to configuration errors.")
        
        # Load game data and initialize systems
        self._initialize_systems()
        
        # Initialize game state
        self.game_state = GameState()
        self.game_state.current_room_id = "hub"
        self.running = False

    def _initialize_systems(self):
        """Load data and initialize all game systems."""
        # Load items
        items_path = self.config_loader.get("file_paths.items_data", "data/items.json")
        try:
            with open(items_path, 'r', encoding='utf-8') as f:
                self.items_data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Items data file not found at '{items_path}'.")
            self.items_data = {}
        
        # Initialize inventory
        max_items = self.config_loader.get("gameplay.max_inventory_items", 10)
        self.inventory = Inventory(self.items_data, max_items)

        # Initialize RoomManager
        rooms_path = self.config_loader.get("file_paths.rooms_data", "data/rooms.json")
        self.room_manager = RoomManager(rooms_path)

    def start(self):
        """Start the main game loop."""
        self.running = True
        self._show_welcome()
        
        while self.running:
            try:
                self._game_loop()
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                if self.config_loader.get("debug.enabled", False):
                    raise
    
    def _show_welcome(self):
        """Display welcome message with proper formatting."""
        separator_char = self.config_loader.get("text_formatting.separator_char", "-")
        separator_length = self.config_loader.get("text_formatting.separator_length", 40)
        separator = separator_char * separator_length
        
        welcome_text = """
Welcome to the Text Adventure!
        
This is a story-driven adventure where you'll explore different paths,
collect meaningful items, and discover multiple endings.

Type 'help' for a list of commands.
Type 'quit' to exit the game.
        """.strip()
        
        print(separator)
        self._format_and_print(welcome_text)
        print(separator)
        print()
    
    def _game_loop(self):
        """Main game loop - get input and process commands."""
        # Show current room
        self._display_current_room()
        
        # Get user input
        prompt = self.config_loader.get("text_formatting.prompt_symbol", "> ")
        user_input = input(prompt).strip().lower()
        
        if not user_input:
            return
            
        # Process command
        self._process_command(user_input)
    
    def _display_current_room(self):
        """Display the current room description using the RoomManager."""
        description = self.room_manager.get_room_description(
            self.game_state.current_room_id, 
            self.game_state
        )
        self._format_and_print(description)
        
        # Show exits if configured
        if self.config_loader.get("display.show_exit_list", True):
            exits = self.room_manager.get_exits_for_room(self.game_state.current_room_id)
            if exits:
                print(f"\nExits: {', '.join(exits.keys())}")
        
        print()
    
    def _format_and_print(self, text: str):
        """Format and print text according to configuration."""
        line_width = self.config_loader.get("text_formatting.line_width", 80)
        paragraph_spacing = self.config_loader.get("text_formatting.paragraph_spacing", 1)
        
        # Simple word wrapping
        words = text.split()
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= line_width:
                current_line += " " + word if current_line else word
            else:
                print(current_line)
                current_line = word
        
        if current_line:
            print(current_line)
            
        # Add paragraph spacing
        for _ in range(paragraph_spacing):
            print()
    
    def _process_command(self, command: str):
        """Process user commands."""
        # A more robust parser would be better, but this works for now.
        parts = command.lower().split()
        if not parts:
            return
            
        action = parts[0]
        target = " ".join(parts[1:]) if len(parts) > 1 else None

        # Command mapping with aliases
        command_map = {
            'help': self._show_help, 'h': self._show_help,
            'look': self._look_around, 'l': self._look_around,
            'inventory': self._show_inventory, 'inv': self._show_inventory, 'i': self._show_inventory,
            'quit': self._quit_game, 'exit': self._quit_game, 'q': self._quit_game,
            'go': self._handle_movement, 'enter': self._handle_movement, 'use': self._handle_movement
        }
        
        if action in command_map:
            # Pass the target to the handler if it exists
            if action in ['go', 'enter', 'use']:
                command_map[action](target)
            else:
                command_map[action]()
        else:
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

    def _handle_movement(self, target_exit: Optional[str]):
        """Handles player movement and checks for locked doors."""
        if not target_exit:
            print("Where would you like to go?")
            return

        current_room = self.room_manager.get_room(self.game_state.current_room_id)
        if not current_room:
            print("Error: Cannot determine current location.")
            return

        # Find the target exit in the current room's exits
        exit_data = None
        for exit_name, data in current_room.exits.items():
            if target_exit in exit_name:
                exit_data = data
                break
        
        if not exit_data:
            print(f"You can't see a '{target_exit}' here.")
            return

        # Check if the door has requirements
        required_item = exit_data.get("requires")
        if required_item:
            if not self.inventory.has_item(required_item):
                # Player doesn't have the key, print the locked message
                locked_message = exit_data.get("locked_message", "The way is blocked.")
                print(locked_message)
                return
        
        # --- Success! Move the player ---
        destination_id = exit_data.get("destination")
        if destination_id:
            print(f"You go through {target_exit}...")
            self.game_state.current_room_id = destination_id
            # Optional: Mark the door as completed/locked behind the player
            # self.game_state.add_completed_door('hub', target_exit)
        else:
            print(f"Error: The exit '{target_exit}' leads nowhere.")

    def _show_help(self):
        """Show available commands."""
        help_text = """
Available Commands:
  look, l          - Look around the current area
  inventory, i     - Check your inventory
  help, h          - Show this help message
  quit, exit, q    - Exit the game
        """.strip()
        
        self._format_and_print(help_text)
    
    def _look_around(self):
        """Look around the current room."""
        self._display_current_room()
    
    def _show_inventory(self):
        """Display inventory contents."""
        if self.inventory.is_empty():
            print("Your inventory is empty.")
            return
        
        print("Inventory:")
        # Loop through the actual Item objects in the inventory
        for item in self.inventory.items:
            print(f"  • {item.name}")
        
        if self.config_loader.get("display.show_item_count_in_inventory", True):
            # Use the inventory's own methods to get count info
            max_items = self.inventory.max_items
            current_count = len(self.inventory.items)
            print(f"\n({current_count}/{max_items} items)")
    
    def _clear_screen(self):
        """Clear the screen (Windows compatible)."""
        os.system('cls')
    
    def _quit_game(self):
        """Exit the game."""
        print("Thank you for playing! Goodbye!")
        self.running = False


def main():
    """Entry point for the game."""
    try:
        game = TextAdventureGame()
        game.start()
    except Exception as e:
        print(f"Failed to start game: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())