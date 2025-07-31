from typing import Tuple, List, Optional, Dict

class CommandParser:
    """
    Parses user input into a standardized command and its arg
    """
    def __init__(self):
        """Initialize the command parser with a dictionary of commands and aliases"""
        self.commands: Dict[str, List[str]] = {
            "help": ["h", "?", "commands"],
            "quit": ["exit", "q"],
            "look": ["l", "examine", "inspect"],
            "go": ["g", "move", "travel"],
            "inventory": ["inv", "i", "items"],
            #"talk": ["t", "speak", "chat"],
            #"use": ["u", "utilize", "apply"],
        }
        
        self._alias_map: Dict[str, str] = {}
        for command, aliases in self.commands.items():
            self._alias_map[command] = command
            for alias in aliases:
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