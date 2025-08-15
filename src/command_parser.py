from typing import Tuple, List, Optional, Dict, Any

class CommandParser:
    """
    Parses user input into a standardized command and its arguments.
    """
    def __init__(self):
        """Initializes the command parser with a dictionary of commands and aliases."""
        self._commands: Dict[str, Dict[str, Any]] = {
            "help": {
                "aliases": ["h", "commands"],
                "description": "Shows a list of commands or help for a specific command.",
                "usage": "help [command]"
            },
            "quit": {
                "aliases": ["q", "exit"],
                "description": "Exits the game.",
                "usage": "quit"
            },
            "look": {
                "aliases": ["l", "examine", "inspect"],
                "description": "Examines the current room or a specific object.",
                "usage": "look [target]"
            },
            "go": {
                "aliases": ["g", "move", "walk"],
                "description": "Moves in a specified direction.",
                "usage": "go <direction>"
            },
            "inventory": {
                "aliases": ["i", "inv"],
                "description": "Checks your inventory.",
                "usage": "inventory"
            },
            "take": {
                "aliases": ["get", "pick", "grab"],
                "description": "Takes an item from the current room.",
                "usage": "take <item>"
            },
            "choose": {
                "aliases": ["select", "pick"],
                "description": "Make a choice during a story segment.",
                "usage": "choose <number>"
            }
        }
        # Create a reverse mapping from alias to canonical command for quick lookups
        self._alias_map: Dict[str, str] = {}
        for command, details in self._commands.items():
            self._alias_map[command] = command
            for alias in details["aliases"]:
                self._alias_map[alias] = command

    def parse(self, user_input: str) -> Tuple[Optional[str], List[str]]:
        """
        parses a raw input string into a canonical command and its arguments.
        
        Args:
            user_input (str): The raw input string from the user.
            
        Returns:
            - Tuple[Optional[str], List[str]]: A tuple containing the command and a list of arguments.
            If the command is not recognized, the first element will be None.
            - A list of arguments, (e.g. ["around"] ["north"])
        """
        words = user_input.lower().strip().split()
        if not words:
            return None, []
        
        verb = words[0]
        args = words[1:]
        
        canonical_command = self._alias_map.get(verb)

        return canonical_command, args

    def get_command_details(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Returns the details for a given command name or alias."""
        canonical_command = self._alias_map.get(command_name)
        if canonical_command:
            return self._commands[canonical_command]
        return None

    def get_all_commands(self) -> Dict[str, Dict[str, Any]]:
        """Returns the full dictionary of commands."""
        return self._commands