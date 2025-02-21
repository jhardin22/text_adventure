import json

class Game:
    def __init__(self):
        self.rooms = {}
        self.game_state = {
            "inventory": [],
            "barred": False,
            "current_room": "start",
            "summary": []
        }
        self.load_rooms("rooms.json")