from src.art import ITEM_ART

ITEM_DETAILS = {
    "Rusty Key": {
        "desc": "A heavy iron key. It has a Yellow '4' scratched on it.",
        "art": ITEM_ART["Rusty Key"],
        "clue": {'char': '4', 'x': 5, 'y': 1, 'color_pair': 3} # Yellow
    },
    "Folded Note": {
        "desc": "A crumpled note. It reads: 'Magenta begins, Blue follows, Yellow is third, Red is fourth, Green ends.'",
        "art": ITEM_ART["Folded Note"],
        "clue": {'char': '3', 'x': 16, 'y': 5, 'color_pair': 2} # Green
    },
    "Dusty Journal": {
        "desc": "An old journal. A Red '2' is embossed on the cover.",
        "art": ITEM_ART["Dusty Journal"],
        "clue": {'char': '2', 'x': 6, 'y': 3, 'color_pair': 4} # Red
    },
    "Riddle Note": {
        "desc": "A scroll with ancient writing.",
        "art": ITEM_ART["Riddle Note"],
        "clue": None
    },
    "Magnifying Glass": {
        "desc": "A glass that makes things look bigger.",
        "art": ITEM_ART["Magnifying Glass"],
        "clue": None
    }
}

class Room:
    def __init__(self, name, description, map_layout, interactables, legend):
        self.name = name
        self.description = description
        self.map_layout = [list(row) for row in map_layout] # Mutable grid
        self.interactables = interactables # Dict mapping char to handler function
        self.legend = legend
        self.width = len(self.map_layout[0])
        self.height = len(self.map_layout)
        self.visited = False
        self.last_interaction_art = None # Store art to display
        self.last_interaction_clue = None # {char, x, y, color_pair}

    def get_char(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.map_layout[y][x]
        return '#'

    def set_char(self, x, y, char):
        if 0 <= y < self.height and 0 <= x < self.width:
            self.map_layout[y][x] = char

# Interaction handlers return (turn_cost, message)
# They can also modify game_state directly

def interact_room1(game_state, char, x, y):
    room = rooms_list[0]
    room.last_interaction_art = None # Reset art
    room.last_interaction_clue = None # Reset clue
    
    # Helper to check if trial passed
    trial_key = f"Trial_{char}_{x}_{y}"
    
    if char == '?': # Search
        if "Lamp Found" not in game_state.flags:
            game_state.flags["Lamp Found"] = True
            game_state.decrease_turns(1)
            room.set_char(x, y, 'L') # Reveal Lamp
            room.last_interaction_art = ITEM_ART.get("Lamp")
            return "You fumble in the dark and find an oil Lamp."
        return "Nothing else here."

    elif char == 'L':
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trial Success! You can now use the Lamp.")
            game_state.start_puzzle("Unscramble", "LIGHT", "Unscramble: G H I L T", success_cb, hint="Opposite of dark")
            return "You attempt to light the lamp..."
            
        if "Lamp" not in game_state.flags:
            game_state.flags["Lamp"] = True
            game_state.decrease_turns(1)
            # Reveal room items
            room.set_char(9, 3, 'C')
            room.set_char(24, 6, 'B')
            room.set_char(30, 11, 'D')
            room.set_char(10, 11, 'R') # Rug
            room.set_char(25, 12, 'P') # Painting
            room.last_interaction_art = ITEM_ART.get("Lamp")
            room.last_interaction_clue = {'char': '4', 'x': 5, 'y': 5, 'color_pair': 3} # Yellow 4
            return "You turn on the lamp. You see a Cabinet, a Bottle, a Rug, a Painting, and a Door. The lamp has a Yellow '4'."
        else:
            room.last_interaction_art = ITEM_ART.get("Lamp")
            room.last_interaction_clue = {'char': '4', 'x': 5, 'y': 5, 'color_pair': 3} # Yellow 4
            return "The lamp buzzes quietly. It has a Yellow '4'."
            
    elif char == 'C': # Cabinet (was Crate)
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trial Success! You pry the cabinet open.")
            game_state.start_puzzle("Unscramble", "CABINET", "Unscramble: T E N I B A C", success_cb, hint="Furniture with shelves")
            return "The cabinet is locked. You try to force it..."

        if "Rusty Key" not in game_state.inventory:
            game_state.add_item("Rusty Key")
            game_state.decrease_turns(1)
            room.last_interaction_art = ITEM_DETAILS["Rusty Key"]["art"]
            room.last_interaction_clue = ITEM_DETAILS["Rusty Key"]["clue"]
            # Reveal Shelves
            room.set_char(3, 7, 'S')
            return "You find a Rusty Key inside. It has a Yellow '4'. You notice some shelves."
        room.last_interaction_art = ITEM_ART.get("Cabinet")
        room.last_interaction_clue = {'char': '2', 'x': 5, 'y': 3, 'color_pair': 4} # Red 2
        return "The cabinet is empty. There is a Red '2' painted on it."

    elif char == 'B': # Bottle (was Barrel)
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trial Success! You uncork the bottle.")
            game_state.start_puzzle("Unscramble", "BOTTLE", "Unscramble: T T L E O B", success_cb, hint="Holds liquids")
            return "The bottle is sealed tight..."

        if "Folded Note" not in game_state.inventory:
            game_state.add_item("Folded Note")
            game_state.decrease_turns(1)
            room.last_interaction_art = ITEM_DETAILS["Folded Note"]["art"]
            room.last_interaction_clue = ITEM_DETAILS["Folded Note"]["clue"]
            # Reveal Shelves
            room.set_char(3, 7, 'S')
            return "You find a Folded Note inside. It has a Green '3'."
        
        room.last_interaction_art = ITEM_ART.get("Bottle")
        room.last_interaction_clue = {'char': '7', 'x': 5, 'y': 3, 'color_pair': 5} # Cyan 7
        return "Just an empty bottle. It has a Cyan '7' on the side."

    elif char == 'S': # Shelves
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trial Success! You can reach the top shelf.")
            game_state.start_puzzle("Unscramble", "DOCUMENT", "Unscramble: T N E M U C O D", success_cb, hint="Paper record")
            return "The shelves are high. You try to reach..."

        if "Dusty Journal" not in game_state.inventory:
            game_state.add_item("Dusty Journal")
            game_state.decrease_turns(1)
            room.last_interaction_art = ITEM_DETAILS["Dusty Journal"]["art"]
            room.last_interaction_clue = ITEM_DETAILS["Dusty Journal"]["clue"]
            # Reveal Floorboards
            room.set_char(16, 10, 'F')
            return "You find a Dusty Journal. It has a Red '2'. It mentions loose floorboards."
        room.last_interaction_art = ITEM_ART.get("Shelves")
        room.last_interaction_clue = {'char': '3', 'x': 5, 'y': 2, 'color_pair': 2} # Green 3
        return "Old dusty shelves. A Green '3' is carved into the wood."

    elif char == 'F': # Floorboards
        # Trial to access floorboards
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trial Success! You pry up the loose board.")
            game_state.start_puzzle("Unscramble", "UNDERNEATH", "Unscramble: H T A E N R E D N U", success_cb, hint="Below something")
            return "The board is stuck tight. You try to pry it..."

        room.last_interaction_art = ITEM_ART.get("Floorboards")
        room.last_interaction_clue = {'char': '5', 'x': 5, 'y': 2, 'color_pair': 6} # Magenta 5
        
        # Actual Puzzle Interaction (requires Code)
        if "Code Solved" not in game_state.flags:
            if "Folded Note" in game_state.inventory:
                def code_success_cb(gs):
                    gs.flags["Code Solved"] = True
                    gs.log("Code Correct! The mechanism unlocks.")
                game_state.start_puzzle("Code", "51423", "Enter the 5-digit code from the note:", code_success_cb, hint="Magenta, Blue, Yellow, Red, Green.")
                return "A combination lock blocks the way. You need a code."
            else:
                return "There is a lock here. You need to find the code sequence."
        
        elif "Code Solved" in game_state.flags:
            return "The floorboards are loose here. The secret compartment is open."

    elif char == 'R': # Rug
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trial Success! You shake out the rug.")
            game_state.start_puzzle("Unscramble", "PATTERN", "Unscramble: T T E R N A P", success_cb, hint="Repeated design")
            return "The rug is heavy with dust..."

        room.last_interaction_art = ITEM_ART.get("Rug")
        room.last_interaction_clue = {'char': '1', 'x': 8, 'y': 2, 'color_pair': 7} # Blue 1
        return "A dusty rug. There is a Blue '1' woven into the pattern."

    elif char == 'P': # Painting
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trial Success! You clean the painting.")
            game_state.start_puzzle("Unscramble", "PORTRAIT", "Unscramble: T R A I T P O R", success_cb, hint="Picture of a person")
            return "The painting is covered in grime..."

        room.last_interaction_art = ITEM_ART.get("Painting")
        room.last_interaction_clue = {'char': '6', 'x': 5, 'y': 2, 'color_pair': 1} # White 6
        return "A faded painting. A White '6' is hidden in the brushstrokes."

    elif char == 'D': # Door
        room.last_interaction_clue = {'char': '7', 'x': 5, 'y': 3, 'color_pair': 5} # Cyan 7
        if "Code Solved" in game_state.flags: 
             if game_state.has_item("Rusty Key"):
                 game_state.current_room_index += 1
                 game_state.decrease_turns(1)
                 room.last_interaction_art = ITEM_ART.get("Door Open")
                 return "You unlock the door and proceed to the Abandoned Library."
             else:
                 room.last_interaction_art = ITEM_ART.get("Door Locked")
                 return "The door is locked. You need a key. It has a Cyan '7'."
        else:
            room.last_interaction_art = ITEM_ART.get("Door Locked")
            return "The door is locked. You see a mechanism linked to the floorboards. It has a Cyan '7'."

    return "Nothing interesting here."

# Room 2: Abandoned Library
def interact_room2(game_state, char, x, y):
    room = rooms_list[1]
    room.last_interaction_art = None
    room.last_interaction_clue = None
    
    trial_key = f"Trial_Room2_{char}_{x}_{y}"

    if char == 'B': # Bookshelves
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Riddle Solved! You find a scroll.")
            game_state.start_puzzle("Riddle", "BOOK", "I have leaves, but no branches. I have a spine, but no bones. What am I?", success_cb, hint="You read it.")
            return "You search the books. A voice whispers a riddle..."

        if "Riddle Note" not in game_state.inventory:
            game_state.add_item("Riddle Note")
            game_state.decrease_turns(1)
            room.last_interaction_art = ITEM_DETAILS["Riddle Note"]["art"]
            return "You find a Riddle Note. You also count 8 distinct volumes on the shelf."
        return "Just dusty books. There are 8 of them."

    elif char == 'K': # Desk
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Riddle Solved! You check the desk.")
            game_state.start_puzzle("Riddle", "DESK", "I have legs but cannot walk. I hold your work but never talk. What am I?", success_cb, hint="You sit at it.")
            return "You approach the desk. A riddle appears on the surface..."

        if "Magnifying Glass" not in game_state.inventory:
            game_state.add_item("Magnifying Glass")
            game_state.decrease_turns(1)
            room.last_interaction_art = ITEM_DETAILS["Magnifying Glass"]["art"]
            return "You find a Magnifying Glass. The desk has 4 sturdy legs."
        return "An empty desk. It has 4 legs."

    elif char == 'S': # Additional Shelves
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Riddle Solved! You examine the shelf.")
            game_state.start_puzzle("Riddle", "CODE", "I am a language without words. I can be broken but never held. What am I?", success_cb, hint="Programmers use it.")
            return "You look at the shelf. Symbols rearrange into a riddle..."

        if "Numeric Clues" not in game_state.flags:
            game_state.flags["Numeric Clues"] = True
            game_state.decrease_turns(2)
            return "You count 6 shelves in total."
        return "There are 6 shelves."

    elif char == 'R': # Riddle Solving Station
        if "Riddle Note" in game_state.inventory and "Magnifying Glass" in game_state.inventory:
            if trial_key not in game_state.flags:
                def success_cb(gs):
                    gs.flags[trial_key] = True
                    gs.flags["Riddle Solved"] = True
                    gs.log("Cipher Solved! The hatch unlocks.")
                # Changed to a Cipher puzzle for variety/difficulty
                game_state.start_puzzle("Code", "LIBRARY", "Decipher the code (Shift +3): O L E U D U B", success_cb, hint="Shift each letter back by 3 (O->L).")
                return "You place the note and glass. A cipher appears..."
            
            return "The cipher is solved. The hatch cover is open."
        else:
            return "You need a Note and a Magnifying Glass to use this station."

    elif char == 'H': # Hatch
        if "Hatch Combo" in game_state.flags:
            game_state.current_room_index += 1
            game_state.decrease_turns(1)
            return "You open the hatch and descend to the Secret Laboratory."
        elif "Riddle Solved" in game_state.flags:
             # Secondary Puzzle: Code from items
            def hatch_success_cb(gs):
                gs.flags["Hatch Combo"] = True
                gs.log("Hatch Unlocked!")
            
            game_state.start_puzzle("Code", "846", "Enter the numeric code (Books, Legs, Shelves):", hatch_success_cb, hint="Count the items in the room.")
            return "The hatch cover is open, but a keypad blocks the way."
        else:
            return "The hatch is locked. You must solve the station riddle first."
            return "Using the glass and note, you solve the multi-step riddle."
        return "You need more clues to solve this riddle."
    return "Nothing interesting."

# Room 3: Secret Laboratory
def interact_room3(game_state, char, x, y):
    trial_key = f"Trial_Room3_{char}_{x}_{y}"
    
    if char == 'C': # Control Panel
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Access Granted.")
            game_state.start_puzzle("Code", "3.1415", "Write the first 5 numbers of pi:", success_cb, hint="3.14...")
            return "The panel blinks..."

        if "Sequence Correct" not in game_state.flags:
            game_state.flags["Sequence Correct"] = True
            return "You input the sequence. Systems online."
        return "Panel is active."

    elif char == 'S': # Chemical Shelves
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("You identify the chemicals.")
            game_state.start_puzzle("Math", "14", "Atomic Number Sum: Carbon(6) + Oxygen(8) = ?", success_cb, hint="6 + 8")
            return "Bottles of strange liquids..."

        if "Chemicals" not in game_state.inventory:
            game_state.add_item("Chemicals")
            game_state.decrease_turns(1)
            return "You carefully take 3 chemicals."
        return "Shelves are empty."

    elif char == 'M': # Mixture Test Station
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Equipment Ready.")
            game_state.start_puzzle("Math", "27", "Volume of a cube with side length 3?", success_cb, hint="3 * 3 * 3")
            return "The station is dormant..."

        if "Chemicals" in game_state.inventory and "Mixture Tested" not in game_state.flags:
            game_state.flags["Mixture Tested"] = True
            game_state.decrease_turns(1)
            return "You test the mixture. It reacts violently and forms crystals: Na Cl."
        return "Mixture is ready. Result: Na Cl."

    elif char == 'K': # Chest
        if "Mixture Tested" in game_state.flags:
            if trial_key not in game_state.flags:
                def success_cb(gs):
                    gs.flags[trial_key] = True
                    gs.log("Chest Unlocked!")
                game_state.start_puzzle("Code", "1117", "Enter the atomic numbers (Na Cl):", success_cb, hint="Sodium(11) Chlorine(17).")
                return "The chest has a keypad..."

            if "Critical Item" not in game_state.inventory:
                game_state.add_item("Critical Item")
                game_state.decrease_turns(1)
                return "The chest opens. You found the Critical Item!"
            return "Empty chest."
        return "The chest is locked. You need the mixture result."

    elif char == 'D': # Door
        if "Critical Item" in game_state.inventory:
            game_state.current_room_index += 1
            game_state.decrease_turns(1)
            return "You unlock the door to the Attic."
        return "Locked. You need the Critical Item."
    return "Nothing interesting."

# Room 4: Forgotten Attic
def interact_room4(game_state, char, x, y):
    trial_key = f"Trial_Room4_{char}_{x}_{y}"

    if char == 'P': # Portraits
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("You move the portrait.")
            game_state.start_puzzle("Trivia", "Portrait", "A painting of a person is called a?", success_cb, hint="Starts with P.")
            return "Dusty portraits watch you..."

        if "Old Key" not in game_state.inventory:
            game_state.add_item("Old Key")
            game_state.decrease_turns(1)
            return "You find an Old Key behind a portrait."
        return "Creepy portraits."

    elif char == 'T': # Trunks
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Trunk mechanism active.")
            game_state.start_puzzle("Trivia", "Key", "You use this to unlock a door.", success_cb, hint="Starts with K.")
            return "A heavy trunk..."

        if "Old Key" in game_state.inventory and "Diary Pages" not in game_state.inventory:
            game_state.add_item("Diary Pages")
            game_state.decrease_turns(1)
            return "You unlock the trunk and find Diary Pages. 'Started at 0800. Worked 4 hours. Break 1 hour. Worked 3 hours. Finished.'"
        elif "Old Key" not in game_state.inventory:
            return "The trunk is locked. You need a key."
        return "Empty trunk."

    elif char == 'N': # Numeric Puzzle
        if "Diary Pages" in game_state.inventory:
            if trial_key not in game_state.flags:
                def success_cb(gs):
                    gs.flags[trial_key] = True
                    gs.flags["Numeric Solved"] = True
                    gs.log("Ladder Released!")
                game_state.start_puzzle("Code", "1600", "Enter the finish time:", success_cb, hint="8+4+1+3 = 16.")
                return "A keypad controls the ladder..."
            return "Ladder is down."
        return "You need clues (Diary) to solve this."

    elif char == 'L': # Ladder (Exit)
        if "Numeric Solved" in game_state.flags:
            game_state.current_room_index += 1
            game_state.decrease_turns(1)
            return "You climb the ladder to the Clock Tower."
        return "The ladder is retracted. Solving the puzzle might release it."
    return "Nothing interesting."

# Room 5: Clock Tower
def interact_room5(game_state, char, x, y):
    trial_key = f"Trial_Room5_{char}_{x}_{y}"

    if char == 'C': # Clock
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Clock Face Open.")
            game_state.start_puzzle("Pattern", "12", "12, 3, 6, 9, ?", success_cb, hint="Clock positions.")
            return "The giant clock face..."

        if "Diary Sequence" not in game_state.flags:
            game_state.flags["Diary Sequence"] = True
            game_state.decrease_turns(1)
            return "You set the gears to align."
        return "Clock is set."

    elif char == 'G': # Gears
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Gears Unjammed.")
            game_state.start_puzzle("Pattern", "Clack", "Click, Clack, Click, ?", success_cb, hint="Sound pattern.")
            return "Massive gears are stuck..."

        if "Diary Sequence" in game_state.flags and "Gears Wound" not in game_state.flags:
            game_state.flags["Gears Wound"] = True
            game_state.decrease_turns(1)
            return "You wind the gears. The mechanism groans to life."
        return "Gears are turning."

    elif char == 'P': # Pendulum
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("Pendulum Released.")
            game_state.start_puzzle("Pattern", "Right", "Left, Right, Left, ?", success_cb, hint="Swing direction.")
            return "The pendulum is held by a lock..."

        if "Gears Wound" in game_state.flags and "Pendulum Active" not in game_state.flags:
            game_state.flags["Pendulum Active"] = True
            game_state.decrease_turns(1)
            return "You activate the pendulum. The final door unlocks."
        return "Pendulum is swinging."

    elif char == 'B': # Bells (New Secondary Puzzle)
        if trial_key not in game_state.flags:
            def success_cb(gs):
                gs.flags[trial_key] = True
                gs.log("The bells chime the first 4 prime numbers.")
            game_state.start_puzzle("Pattern", "Ding", "Dong, Ding, Dong, ?", success_cb, hint="Bell sound.")
            return "A set of chimes..."
        return "The bells chime the first 4 prime numbers."

    elif char == 'D': # Final Door
        if "Pendulum Active" in game_state.flags:
            # Secondary Puzzle Check
            if "Final Code Solved" not in game_state.flags:
                 def success_cb(gs):
                    gs.flags["Final Code Solved"] = True
                    gs.victory = True
                    gs.decrease_turns(1)
                 game_state.start_puzzle("Code", "2357", "Enter the chime melody code:", success_cb, hint="Primes: 2, 3, 5, 7.")
                 return "The door has a final lock..."
            else:
                return "You open the final door and ESCAPE!"
        return "The door is sealed tight."
    return "Nothing interesting."

def create_rooms():
    room1_map = [
        "+--------------------------------+",
        "| ?                              |",
        "|      .---.                     |",
        "|      |   |                     |",
        "|      '---'                     |",
        "|                      ( )       |",
        "|                     /   \\      |",
        "| [===]                          |",
        "| [===]                          |",
        "|              ###               |",
        "|              ###               |",
        "|      [~~~~~]                   |",
        "|      [~~~~~]         [P]       |",
        "+--------------------------------+"
    ]
    room1_legend = {
        '?': 'Search Dark Room',
        'L': 'Lamp',
        'C': 'Cabinet',
        'B': 'Bottle',
        'S': 'Shelves',
        'F': 'Floorboards',
        'R': 'Rug',
        'P': 'Painting',
        'D': 'Door'
    }

    room2_map = [
        "+--------------------------------+",
        "|  ===   ===   ===   ===   ===   |",
        "|  |B|   | |   | |   | |   |S|   |",
        "|  ===   ===   ===   ===   ===   |",
        "|                                |",
        "|      [_______]                 |",
        "|      [   K   ]                 |",
        "|      [_______]                 |",
        "|                                |",
        "|           ( R )                |",
        "|                                |",
        "|                              H |",
        "+--------------------------------+"
    ]
    room2_legend = {
        'B': 'Bookshelves',
        'K': 'Desk',
        'S': 'Shelves',
        'R': 'Riddle Station',
        'H': 'Hatch'
    }

    room3_map = [
        "+--------------------------------+",
        "|  [C]   [S]   [ ]   [ ]   [ ]   |",
        "|  | |   | |   | |   | |   | |   |",
        "|  |_|   |_|   |_|   |_|   |_|   |",
        "|                                |",
        "|      /---\\                     |",
        "|      | M |                     |",
        "|      \\---/                     |",
        "|                                |",
        "|  [ K ]                         |",
        "|                                |",
        "|                              D |",
        "+--------------------------------+"
    ]
    room3_legend = {
        'C': 'Control Panel',
        'S': 'Chemical Shelves',
        'M': 'Mixture Station',
        'K': 'Chest',
        'D': 'Door'
    }

    room4_map = [
        "+--------------------------------+",
        "|  [P]   / \\   [ ]   / \\   [T]   |",
        "|       /   \\       /   \\        |",
        "|                                |",
        "|           [ N ]                |",
        "|                                |",
        "|      ( )           ( )         |",
        "|     /   \\         /   \\        |",
        "|                                |",
        "|                              L |",
        "+--------------------------------+"
    ]
    room4_legend = {
        'P': 'Portraits',
        'T': 'Trunks',
        'N': 'Numeric Puzzle',
        'L': 'Ladder'
    }

    room5_map = [
        "+--------------------------------+",
        "|            (12)                |",
        "|           /    \\               |",
        "|  (C)     |  .   |     (G)      |",
        "|           \\    /               |",
        "|            (06)                |",
        "|                                |",
        "|             |                  |",
        "|            (P)                 |",
        "|                                |",
        "|  [B]                         D |",
        "+--------------------------------+"
    ]
    room5_legend = {
        'C': 'Clock',
        'G': 'Gears',
        'P': 'Pendulum',
        'B': 'Bells',
        'D': 'Final Door'
    }

    return [
        Room("Dark Cellar", "A cold, dark room.", room1_map, interact_room1, room1_legend),
        Room("Abandoned Library", "Books everywhere.", room2_map, interact_room2, room2_legend),
        Room("Secret Laboratory", "Bubbling beakers.", room3_map, interact_room3, room3_legend),
        Room("Forgotten Attic", "Dusty and old.", room4_map, interact_room4, room4_legend),
        Room("Clock Tower", "Tick tock.", room5_map, interact_room5, room5_legend),
    ]

rooms_list = create_rooms()

def reset_rooms():
    global rooms_list
    rooms_list[:] = create_rooms()
