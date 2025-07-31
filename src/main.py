"""
Text Adventure Game - Main Entry Point
A love letter text adventure with linear storytelling.
"""

from typing import Optional
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import TextAdventure


def main() -> None:
    """Main entry point for the text adventure game."""
    print("=" * 60)
    print("Welcome to the Text Adventure!")
    print("A story of love, discovery, and adventure...")
    print("=" * 60)
    print()
    
    try:
        game = TextAdventure()
        game.run()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check your game files and try again.")
    finally:
        print("\nGame ended.")


if __name__ == "__main__":
    main()