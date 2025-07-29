# Text Adventure

This is a text-based adventure. This project is intended to be a teaching tool for the developer, but it's also a love letter to their wife. This is a linear text adventure with only a couple of paths for various outcomes.

## Instructions for Copilot

 Iteratively guide the developer through building this game with the below considerations. Explain the concepts as development progresses, providing practical and alternate examples of required concepts. Break each iteration down into tasks that can be added as Github issues to track the development of the game as it grows. If a new conversation is started with these instructions, start with a brief overview of the game and its design goals, then ask if you should start with the first task or if the developer has a specific area they want to focus on or pick up from. If the developer gives you a starting point when providing these instructions, start with that point and work through the tasks iteratively.

### Design Goals
- The game should be simple and linear, with a focus on storytelling rather than complex mechanics.
- The player should be able to navigate through the game using simple text commands.
- The game should have a simple command line interface, with `help`, giving a list of actions for the player to take.
- The game should be written in Python, using a simple text-based interface.
- There are rooms in the game, but they aren't really rooms, they are just different story points in the game; The door for the room is an object that checks if the player has the right item to open it.
- There is one "hub" room. There's a talking dog in this room that gives the player hints and advice.
- There are three doors in the hub room, intended to be acccessed in a specific order.
- Behind each door is a small part of the story, with two or three branches leading to different items.
- After the player has collected the items, the player is sent back to the hub room with relevant story information, and that door is locked.
- The item a player gets from each door is used to open the next door, and the process repeats until all three doors have been opened.
- When the item from the third door is collected, the player can leave the hub room to recieve an ending, or the can return to the first room, which will give them a different ending.

### Game Structure
- Events in rooms should be simple and linear.
- The game should have a simple command structure, with commands like `look`, `go`, `take`, and `use`.
- The inventory should be accessible via a command like `inventory` or `i` as a menu where items can be `examined`.
- The game should have a simple inventory system, where the player can collect items. They are more for story purposes than for mechanics; The items have flavor text that enhances the narrative or gives a hint about the next step.
- The game should have a simple save and load system, allowing the player to save their progress and return to it later.
- Each room should have a progressive piece of the story, with no more than three branches leading to different items.

### Code Organization
- Use a modular structure with separate files for game logic, room management, inventory, and save/load functionality
- Implement a Room base class that can be inherited by specific room types
- Implement a simple item class for inventory management
- Use a JSON file to store room descriptions, item details, and game state
- Use type hints throughout the codebase for better maintainability
- Follow PEP 8 style guidelines

### Error Handling
- Gracefully handle invalid commands with helpful feedback
- Validate save file integrity before loading
- Handle file I/O errors for save/load and text data

### Testing
- Include unit tests for core game mechanics (inventory, room transitions, save/load)
- Test edge cases like invalid inputs and corrupted save files

### Configuration
- Store game settings (like file paths) in a separate config file
- Make text formatting and display options configurable

### Player Experience
- Each interaction should provide clear feedback about what happened
- Commands should be forgiving (accept variations like "examine" and "look")
- Provide contextual hints when players seem stuck
- Include a brief tutorial or introduction explaining basic commands

### Story Coherence
- Each door's story should build toward the overall narrative
- The talking dog's hints should be contextual to the player's current progress
- Ensure the two different endings feel meaningfully different and satisfying
- Include emotional beats that connect to the "love letter" theme

### Accessibility
- Support both full commands ("look around") and abbreviations ("l")
- Provide clear descriptions of the current state after each action
- Include an "inventory" or "status" command to check current items and progress

### Balance and Pacing
- Each door section should take roughly the same amount of time to complete
- Ensure no single choice feels obviously "wrong" - make branches feel meaningful
- Limit the number of commands needed to progress to avoid tedium

### Quality of Life
- Include an "undo" command for accidental actions
- Allow players to re-read recent text or important story moments
- Provide clear indication when a door becomes locked after completion



