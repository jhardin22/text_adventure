"""
Basic tests to verify project structure is working.
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import TextAdventure
from inventory import Item, Inventory
from room import HubRoom


class TestBasicStructure(unittest.TestCase):
    """Test basic project structure and imports."""
    
    def test_game_initialization(self):
        """Test that the game can be initialized."""
        game = TextAdventure()
        self.assertIsNotNone(game)
        self.assertEqual(game.current_room, "hub")
        self.assertFalse(game.running)
    
    def test_inventory_creation(self):
        """Test inventory can be created and used."""
        inventory = Inventory()
        self.assertTrue(inventory.is_empty())
        self.assertEqual(inventory.count(), 0)
    
    def test_item_creation(self):
        """Test items can be created."""
        item = Item("test_key", "Mysterious Key", "A small, ornate key.")
        self.assertEqual(item.item_id, "test_key")
        self.assertEqual(item.name, "Mysterious Key")
    
    def test_hub_room_creation(self):
        """Test hub room can be created."""
        hub = HubRoom()
        self.assertEqual(hub.room_id, "hub")
        self.assertEqual(hub.name, "The Hub")
        self.assertFalse(hub.visited)


if __name__ == '__main__':
    unittest.main()