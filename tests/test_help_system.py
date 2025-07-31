import unittest
from unittest.mock import patch
import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.game import TextAdventure

class TestHelpSystem(unittest.TestCase):
    """Tests for the dynamic help system."""

    def setUp(self):
        """Set up a new game instance for each test."""
        self.game = TextAdventure()

    @patch('builtins.print')
    def test_general_help(self, mock_print):
        """Test that the general 'help' command lists all commands."""
        self.game._show_help([])
        
        output = " ".join(call.args[0] for call in mock_print.call_args_list if call.args)
        
        # Check that descriptions for key commands are present
        self.assertIn("Exits the game.", output)
        self.assertIn("Examines the current room", output)
        self.assertIn("Checks your inventory.", output)

    @patch('builtins.print')
    def test_specific_help_for_look(self, mock_print):
        """Test that 'help look' shows detailed help for the look command."""
        self.game._show_help(['look'])
        
        output = " ".join(call.args[0] for call in mock_print.call_args_list if call.args)
        
        self.assertIn("Usage: look [target]", output)
        self.assertIn("Aliases: l, examine, inspect", output)

    @patch('builtins.print')
    def test_specific_help_for_alias(self, mock_print):
        """Test that 'help i' shows detailed help for the inventory command."""
        self.game._show_help(['i'])
        
        output = " ".join(call.args[0] for call in mock_print.call_args_list if call.args)
        
        self.assertIn("Usage: inventory", output)
        self.assertIn("Description: Checks your inventory.", output)

    @patch('builtins.print')
    def test_help_for_unknown_command(self, mock_print):
        """Test that asking for help on an unknown command gives an error."""
        self.game._show_help(['fly'])
        
        output = " ".join(call.args[0] for call in mock_print.call_args_list if call.args)
        
        self.assertIn("is not a recognized command", output)

if __name__ == '__main__':
    unittest.main()