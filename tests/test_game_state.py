import unittest
import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.game_state import GameState

class TestGameState(unittest.TestCase):
    """Tests for the GameState class."""

    def setUp(self):
        """Create a fresh GameState instance for each test."""
        self.state = GameState()

    def test_initial_state(self):
        """Test that the game state initializes with correct default values."""
        self.assertEqual(self.state.current_room_id, "hub")
        self.assertEqual(self.state.inventory_ids, set())
        self.assertEqual(self.state.completed_doors, set())
        self.assertEqual(self.state.game_flags, {})

    def test_item_management(self):
        """Test adding and checking for items."""
        self.assertFalse(self.state.has_item("key_1"))
        self.state.add_item("key_1")
        self.assertTrue(self.state.has_item("key_1"))
        # Adding again should not cause an error or duplicates
        self.state.add_item("key_1")
        self.assertEqual(len(self.state.inventory_ids), 1)

    def test_door_completion(self):
        """Test marking a door as completed."""
        self.assertFalse(self.state.is_door_completed("door_north"))
        self.state.complete_door("door_north")
        self.assertTrue(self.state.is_door_completed("door_north"))

    def test_flag_management(self):
        """Test setting and getting game flags."""
        self.assertIsNone(self.state.get_flag("dog_spoken"))
        self.state.set_flag("dog_spoken", True)
        self.assertTrue(self.state.get_flag("dog_spoken"))
        self.state.set_flag("player_score", 100)
        self.assertEqual(self.state.get_flag("player_score"), 100)

if __name__ == '__main__':
    unittest.main()