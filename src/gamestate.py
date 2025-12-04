class GameState:
    def __init__(self):
        self.turns_remaining = 150
        self.current_room_index = 0
        self.inventory = []
        self.flags = {}
        self.game_over = False
        self.victory = False
        self.active_puzzle = None # { "type": "unscramble", "target": "word", "prompt": "Unscramble this...", "callback": func }
        self.message_log = ["Welcome to Blackout Escape!", "You have 150 turns to escape."]
        
    def start_puzzle(self, puzzle_type, target, prompt, callback, hint=None):
        self.active_puzzle = {
            "type": puzzle_type,
            "target": target,
            "prompt": prompt,
            "callback": callback,
            "input_buffer": "",
            "hint": hint,
            "hint_shown": False
        }
        self.log(f"Trial Started: {prompt}")

    def resolve_puzzle(self, success):
        puzzle = self.active_puzzle
        self.active_puzzle = None
        if success:
            self.log("Trial Passed!")
            if puzzle["callback"]:
                puzzle["callback"](self)
        else:
            self.log("Trial Failed. You lost a turn.")
            self.decrease_turns(1)

    def log(self, message):
        self.message_log.append(message)
        if len(self.message_log) > 5:
            self.message_log.pop(0)

    def decrease_turns(self, amount):
        self.turns_remaining -= amount
        if self.turns_remaining <= 0:
            self.turns_remaining = 0
            self.game_over = True
            self.log("You have run out of time! darkness consumes you.")

    def has_item(self, item_name):
        return item_name in self.inventory

    def add_item(self, item_name):
        if item_name not in self.inventory:
            self.inventory.append(item_name)
            self.log(f"Picked up: {item_name}")
            
    def remove_item(self, item_name):
        if item_name in self.inventory:
            self.inventory.remove(item_name)
