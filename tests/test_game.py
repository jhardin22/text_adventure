import unittest
from unittest.mock import patch
import os, sys

from src.game import TextAdventure
from src.inventory import Item, Inventory
from src.room import HubRoom

class TestGame(unittest.TestCase):
    """
    Tests for the main TextAdventure game class.
    """
    
    def setUp(self):
        """Set up a new game instance for each test."""
        self.game = TextAdventure()
        
    def test_room_loading(self):
        """Test that rooms are loaded correctly."""
        self.assertIn("hub", self.game.rooms)
        self.assertIsInstance(self.game.rooms["hub"], HubRoom)
        self.assertEqual(self.game.current_room.room_id, "hub")
        
    def test_look_command(self):
        """Test that the look command prints room details."""
        with patch('builtins.print') as mock_print:
            self.game._look_around()
            
            # Check that the output contains parts of the expected data
            output = " ".join(call.args[0] for call in mock_print.call_args_list)
            self.assertIn("cavern. There's", output)
            self.assertIn("set into the rock", output)
            self.assertIn("white dog lays", output)