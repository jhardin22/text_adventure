"""
Core game logic for the text adventure.
"""

from typing import Dict, Any, Optional
import json
import os
from pathlib import Path


class TextAdventure:
    """Main game class that manages the overall game state and flow."""
    
    def __init__(self) -> None:
        """Initialize the game with configuration and starting state."""
        self.config: Dict[str, Any] = self._load_config()
        self.running: bool = False
        self.current_room: str = "hub"
        self.game_state: Dict[str, Any] = {
            "player_name": "",
            "current_room": "hub",
            "inventory": [],
            "doors_completed": [],
            "game_flags": {}
        }
    
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
        print("A friendly dog approaches you with a wagging tail.")
        print()
        print("Type 'help' for a list of commands.")
        print("Type 'quit' to exit the game.")
        print()
    
    def _process_command(self, command: str) -> None:
        """Process a player command."""
        command = command.lower().strip()
        
        # Basic commands for now
        if command in ['quit', 'exit', 'q']:
            print("Thanks for playing!")
            self.running = False
        elif command in ['help', 'h']:
            self._show_help()
        elif command in ['look', 'l']:
            self._look_around()
        else:
            print(f"I don't understand '{command}'. Type 'help' for available commands.")
    
    def _show_help(self) -> None:
        """Display available commands."""
        print("\nAvailable Commands:")
        print("  help, h      - Show this help message")
        print("  look, l      - Look around the current area")
        print("  quit, exit   - Quit the game")
        print()
    
    def _look_around(self) -> None:
        """Display the current room description."""
        print("\nYou are in the hub room.")
        print("A friendly dog sits nearby, tail wagging expectantly.")
        print("You see three mysterious doors around the room.")
        print()