import unittest
import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.command_parser import CommandParser

class TestCommandParser(unittest.TestCase):
    """Tests for the CommandParser class."""

    def setUp(self):
        """Set up a new parser for each test."""
        self.parser = CommandParser()

    def test_basic_command(self):
        """Test a simple, single-word command."""
        command, args = self.parser.parse("look")
        self.assertEqual(command, "look")
        self.assertEqual(args, [])

    def test_command_with_alias(self):
        """Test that an alias is correctly mapped to its canonical command."""
        command, args = self.parser.parse("l")
        self.assertEqual(command, "look")
        self.assertEqual(args, [])

    def test_multi_word_command(self):
        """Test a command with arguments."""
        command, args = self.parser.parse("go north")
        self.assertEqual(command, "go")
        self.assertEqual(args, ["north"])

    def test_case_insensitivity(self):
        """Test that the parser is case-insensitive."""
        command, args = self.parser.parse("GO NORTH")
        self.assertEqual(command, "go")
        self.assertEqual(args, ["north"])

    def test_extra_whitespace(self):
        """Test that the parser handles extra whitespace."""
        command, args = self.parser.parse("  look   around  ")
        self.assertEqual(command, "look")
        self.assertEqual(args, ["around"])

    def test_unknown_command(self):
        """Test that an unknown command returns None."""
        command, args = self.parser.parse("fly")
        self.assertIsNone(command)
        self.assertEqual(args, [])

    def test_empty_input(self):
        """Test that empty input returns None."""
        command, args = self.parser.parse("")
        self.assertIsNone(command)
        self.assertEqual(args, [])

if __name__ == '__main__':
    unittest.main()