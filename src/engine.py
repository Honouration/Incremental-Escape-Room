import curses
import time
import textwrap
from src.rooms import rooms_list, reset_rooms, ITEM_DETAILS
from src.gamestate import GameState

class GameEngine:
    def __init__(self, stdscr, game_state):
        self.stdscr = stdscr
        self.game_state = game_state
        self.player_x = 1
        self.player_y = 1
        self.current_room = rooms_list[self.game_state.current_room_index]
        self.state = "TITLE" # TITLE, GAME, GAMEOVER, VICTORY
        self.inventory_selection_index = 0
        self.debug_buffer = ""

        # Colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Player / Green
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Interactables / Yellow
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK) # Walls / Red
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK) # Cyan
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Magenta
        curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK) # Blue

        self.stdscr.clear()
        self.stdscr.keypad(True)
        curses.curs_set(0) # Hide default cursor
        
        # Enable mouse events
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        # Note: Mouse support in Windows terminals can be dependent on the terminal emulator used.
        
        # Set non-blocking input with timeout (100ms)
        self.stdscr.timeout(100)
        self.last_turn_decay = time.time()

    def run(self):
        while True:
            if self.state == "TITLE":
                self.render_title_screen()
                key = self.stdscr.getch()
                if key != -1:
                    self.state = "GAME"
            elif self.state == "GAME":
                if time.time() - self.last_turn_decay >= 30:
                    self.game_state.decrease_turns(1)
                    self.last_turn_decay = time.time()

                if self.game_state.game_over:
                    self.state = "GAMEOVER"
                elif self.game_state.victory:
                    self.state = "VICTORY"
                elif self.game_state.active_puzzle:
                    self.render_puzzle()
                    self.handle_puzzle_input()
                else:
                    self.render()
                    self.handle_input()
                    
                    # Check if room changed
                    if rooms_list[self.game_state.current_room_index] != self.current_room:
                        self.current_room = rooms_list[self.game_state.current_room_index]
                        self.player_x = 1
                        self.player_y = 1 # Reset position for new room (simplified)
            elif self.state == "INVENTORY":
                self.render_inventory_menu()
                self.handle_inventory_input()
            elif self.state == "PAUSE":
                self.render_pause_screen()
                key = self.stdscr.getch()
                if key == ord('p') or key == 27: # p or ESC
                    self.state = "GAME"
                elif key == ord('r'):
                    self.reset_game()
                elif key == ord('q'):
                    break
                elif key == ord('D'): # Hidden debug trigger
                    self.state = "DEBUG_PASSWORD"
                    self.debug_buffer = ""
            elif self.state == "DEBUG_PASSWORD":
                self.render_debug_password()
                self.handle_debug_password_input()
            elif self.state == "DEBUG_SELECT":
                self.render_debug_select()
                self.handle_debug_select_input()
            elif self.state in ["GAMEOVER", "VICTORY"]:
                self.render_end_screen()
                key = self.stdscr.getch()
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.reset_game()

    def reset_game(self):
        reset_rooms()
        self.game_state = GameState()
        self.current_room = rooms_list[self.game_state.current_room_index]
        self.player_x = 1
        self.player_y = 1
        self.state = "GAME"
        self.last_turn_decay = time.time()

    def render_title_screen(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        title_art = [
            r"  ____  _            _               _   ",
            r" |  _ \| |          | |             | |  ",
            r" | |_) | | __ _  ___| | _____  _   _| |_ ",
            r" |  _ <| |/ _` |/ __| |/ / _ \| | | | __|",
            r" | |_) | | (_| | (__|   < (_) | |_| | |_ ",
            r" |____/|_|\__,_|\___|_|\_\___/ \__,_|\__|",
            r"  ______                          ",
            r" |  ____|                         ",
            r" | |__   ___  ___ __ _ _ __   ___ ",
            r" |  __| / __|/ __/ _` | '_ \ / _ \ ",
            r" | |____\__ \ (_| (_| | |_) |  __/",
            r" |______|___/\___\__,_| .__/ \___|",
            r"                      | |         ",
            r"                      |_|         "
        ]
        
        start_y = max(0, (height - len(title_art)) // 2 - 2)
        for i, line in enumerate(title_art):
            if start_y + i < height:
                start_x = max(0, (width - len(line)) // 2)
                self.stdscr.addstr(start_y + i, start_x, line, curses.A_BOLD)
        
        msg = "Press any key to start"
        if start_y + len(title_art) + 2 < height:
            self.stdscr.addstr(start_y + len(title_art) + 2, (width - len(msg)) // 2, msg, curses.A_BLINK)
        
        self.stdscr.refresh()

    def render(self):
        self.stdscr.erase()
        
        # Draw UI
        height, width = self.stdscr.getmaxyx()
        
        # Title
        title = f"Blackout Escape - {self.current_room.name} (Click or Bump to Interact)"
        self.stdscr.addstr(0, 0, title, curses.A_BOLD)
        
        # Stats
        stats = f"Turns: {self.game_state.turns_remaining} | [I]nventory | [P]ause | [R]eset"
        self.stdscr.addstr(1, 0, stats)
        
        # Draw Map
        # Offset map to not overwrite UI
        map_offset_y = 3
        for y, row in enumerate(self.current_room.map_layout):
            for x, char in enumerate(row):
                if char in ['#', '-', '|', '+']:
                    self.stdscr.addch(y + map_offset_y, x, char, curses.color_pair(4))
                elif char == ' ':
                    self.stdscr.addch(y + map_offset_y, x, char, curses.color_pair(1))
                else:
                    self.stdscr.addch(y + map_offset_y, x, char, curses.color_pair(3))
        
        # Draw Player
        self.stdscr.addch(self.player_y + map_offset_y, self.player_x, '@', curses.color_pair(2) | curses.A_BOLD)

        # Draw Legend
        legend_offset_x = self.current_room.width + 5
        self.stdscr.addstr(map_offset_y, legend_offset_x, "Legend:", curses.A_UNDERLINE)
        for i, (char, desc) in enumerate(self.current_room.legend.items()):
            self.stdscr.addstr(map_offset_y + 1 + i, legend_offset_x, f"{char}: {desc}")

        # Draw Item Art (if any)
        if self.current_room.last_interaction_art:
            art = self.current_room.last_interaction_art
            art_offset_x = legend_offset_x + 25  # To the right of legend
            for i, line in enumerate(art):
                if map_offset_y + i < height:
                    self.stdscr.addstr(
                        map_offset_y + i,
                        art_offset_x,
                        line,
                        curses.color_pair(3)
                    )
            
            # Draw Clue Overlay if present
            if hasattr(self.current_room, 'last_interaction_clue') and self.current_room.last_interaction_clue:
                clue = self.current_room.last_interaction_clue
                clue_y = map_offset_y + clue['y']
                clue_x = art_offset_x + clue['x']
                if clue_y < height:
                    self.stdscr.addch(
                        clue_y,
                        clue_x,
                        clue['char'],
                        curses.color_pair(clue['color_pair']) | curses.A_BOLD
                    )

        # Draw Log
        log_offset_y = map_offset_y + self.current_room.height + 2
        self.stdscr.addstr(log_offset_y, 0, "Log:", curses.A_UNDERLINE)
        for i, msg in enumerate(self.game_state.message_log):
            if log_offset_y + 1 + i < height:
                style = curses.A_BOLD | curses.color_pair(3) if i == len(self.game_state.message_log) - 1 else curses.A_NORMAL
                self.stdscr.addstr(log_offset_y + 1 + i, 0, f"- {msg}", style)

        self.stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()
        
        if key == -1:
            return # Timeout
        
        new_x, new_y = self.player_x, self.player_y
        
        if key == curses.KEY_UP:
            new_y -= 1
        elif key == curses.KEY_DOWN:
            new_y += 1
        elif key == curses.KEY_LEFT:
            new_x -= 1
        elif key == curses.KEY_RIGHT:
            new_x += 1
        elif key == ord('q'):
            self.game_state.game_over = True
            return
        elif key == ord('p'):
            self.state = "PAUSE"
            return
        elif key == ord('i'):
            self.state = "INVENTORY"
            self.inventory_selection_index = 0
            return
        elif key == curses.KEY_MOUSE:
            try:
                _, mx, my, _, _ = curses.getmouse()
                
                # Check for UI clicks (Top Bar)
                if my == 1:
                    # "Turns: ... | [I]nventory | [P]ause | [R]eset"
                    # We need to approximate the x positions.
                    # Stats string starts at x=0.
                    # Let's assume standard width for turns part, or just check ranges.
                    # A safer way is to check the text at that position, but we can't easily read back.
                    # Let's use broad ranges based on the string length.
                    # "Turns: 150 | " is approx 13 chars.
                    # "[I]nventory" is 11 chars.
                    # "[P]ause" is 7 chars.
                    # "[R]eset" is 7 chars.
                    # Separators " | " are 3 chars.
                    
                    # Simplified hit detection:
                    # Inventory starts around x=13 (variable based on turns digits)
                    # Let's just check if x is in the right half of the screen or specific zones.
                    # Better: Reconstruct the string to find indices.
                    stats = f"Turns: {self.game_state.turns_remaining} | [I]nventory | [P]ause | [R]eset"
                    inv_index = stats.find("[I]nventory")
                    pause_index = stats.find("[P]ause")
                    reset_index = stats.find("[R]eset")
                    
                    if inv_index != -1 and inv_index <= mx < inv_index + 11:
                        self.state = "INVENTORY"
                        self.inventory_selection_index = 0
                        return
                    elif pause_index != -1 and pause_index <= mx < pause_index + 7:
                        self.state = "PAUSE"
                        return
                    elif reset_index != -1 and reset_index <= mx < reset_index + 7:
                        self.reset_game()
                        return

                # Translate to map coordinates
                # map is drawn at map_offset_y = 3
                map_y = my - 3
                map_x = mx
                
                if 0 <= map_y < self.current_room.height and 0 <= map_x < self.current_room.width:
                    # Clicked inside map
                    char_at_target = self.current_room.get_char(map_x, map_y)
                    if char_at_target not in ['#', ' ', '-', '|', '+']:
                        # It's an interactable
                        handler = self.current_room.interactables
                        msg = handler(self.game_state, char_at_target, map_x, map_y)
                        self.game_state.log(f"Clicked: {msg}")
            except curses.error:
                pass
            return # Mouse handled

        # Check bounds and collisions
        char_at_target = self.current_room.get_char(new_x, new_y)
        
        if char_at_target in ['#', '-', '|', '+']:
            return # Wall, do nothing
            
        elif char_at_target == ' ':
            self.player_x = new_x
            self.player_y = new_y
            pass
            
        else:
            # Interaction
            # Call the interaction handler for the room
            # We need to pass the char to the handler
            handler = self.current_room.interactables
            # In rooms.py I defined interactables as a function `interact_room1`
            # So self.current_room.interactables is that function
            
            msg = handler(self.game_state, char_at_target, new_x, new_y)
            self.game_state.log(msg)

    def render_puzzle(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        puzzle = self.game_state.active_puzzle
        self.hint_button_rect = None
        
        # Draw Box
        box_width = 60
        box_height = 14  # Increased height for hints/wrapping
        start_y = (height - box_height) // 2
        start_x = (width - box_width) // 2
        
        # Draw borders
        for y in range(start_y, start_y + box_height):
            for x in range(start_x, start_x + box_width):
                if y == start_y or y == start_y + box_height - 1:
                    self.stdscr.addch(y, x, '-')
                elif x == start_x or x == start_x + box_width - 1:
                    self.stdscr.addch(y, x, '|')
        
        # Title
        title = f" TRIAL: {puzzle['type'].upper()} "
        self.stdscr.addstr(start_y, start_x + (box_width - len(title)) // 2, title, curses.A_BOLD)
        
        # Prompt (Wrapped)
        prompt = puzzle['prompt']
        wrapped_lines = textwrap.wrap(prompt, box_width - 4)
        for i, line in enumerate(wrapped_lines):
            if start_y + 2 + i < start_y + box_height - 4: # Prevent overflow
                self.stdscr.addstr(start_y + 2 + i, start_x + 2, line)
        
        current_y = start_y + 2 + len(wrapped_lines) + 1

        # Hint Display
        if puzzle.get('hint'):
            if puzzle.get('hint_shown'):
                hint_text = f"HINT: {puzzle['hint']}"
                self.stdscr.addstr(current_y, start_x + 2, hint_text, curses.A_ITALIC)
            else:
                hint_msg = "[ GET HINT (-1 Turn) ]"
                hint_x = start_x + (box_width - len(hint_msg)) // 2
                self.stdscr.addstr(current_y, hint_x, hint_msg, curses.A_BOLD | curses.color_pair(3))
                self.hint_button_rect = (hint_x, current_y, len(hint_msg), 1)
            current_y += 2

        # Input Field
        input_label = "Answer: "
        self.stdscr.addstr(current_y, start_x + 2, input_label)
        self.stdscr.addstr(current_y, start_x + 2 + len(input_label), puzzle['input_buffer'] + "_", curses.A_BLINK)
        
        # Instructions
        instr = "Press ENTER to submit"
        self.stdscr.addstr(start_y + box_height - 2, start_x + (box_width - len(instr)) // 2, instr, curses.A_DIM)
        
        self.stdscr.refresh()

    def handle_puzzle_input(self):
        key = self.stdscr.getch()
        if key == -1:
            return
            
        puzzle = self.game_state.active_puzzle
        
        if key == curses.KEY_MOUSE:
            try:
                _, mx, my, _, _ = curses.getmouse()
                if self.hint_button_rect:
                    bx, by, bw, bh = self.hint_button_rect
                    if by <= my < by + bh and bx <= mx < bx + bw:
                        # Clicked hint button
                        if puzzle.get('hint') and not puzzle.get('hint_shown'):
                            if self.game_state.turns_remaining > 0:
                                self.game_state.decrease_turns(1)
                                puzzle['hint_shown'] = True
                                self.game_state.log("Hint used! -1 Turn")
                            else:
                                self.game_state.log("Not enough turns for hint!")
            except curses.error:
                pass
            return

        if key == 10 or key == 13: # Enter
            # Check answer
            if puzzle['input_buffer'].lower().strip() == puzzle['target'].lower().strip():
                self.game_state.resolve_puzzle(True)
            else:
                self.game_state.resolve_puzzle(False)
        elif key == 8 or key == 127 or key == curses.KEY_BACKSPACE: # Backspace
            puzzle['input_buffer'] = puzzle['input_buffer'][:-1]
        elif 32 <= key <= 126: # Printable chars
            puzzle['input_buffer'] += chr(key)

    def render_end_screen(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        if self.game_state.victory:
            art = [
                r" __      __ _      _                   _ ",
                r" \ \    / /(_)    | |                 | |",
                r"  \ \  / /  _  ___| |_ ___  _ __ _   _| |",
                r"   \ \/ /  | |/ __| __/ _ \| '__| | | | |",
                r"    \  /   | | (__| || (_) | |  | |_| |_|",
                r"     \/    |_|\___|\__\___/|_|   \__, (_) ",
                r"                                  __/ |  ",
                r"                                 |___/   "
            ]
            msg = "CONGRATULATIONS! YOU ESCAPED!"
            color = curses.color_pair(2)
        else:
            art = [
                r"   _____                         ____                 ",
                r"  / ____|                       / __ \                ",
                r" | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ ",
                r" | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|",
                r" | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   ",
                r"  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   "
            ]
            msg = "GAME OVER. DARKNESS CONSUMED YOU."
            color = curses.color_pair(4)
            
        start_y = max(0, (height - len(art)) // 2 - 2)
        for i, line in enumerate(art):
            if start_y + i < height:
                start_x = max(0, (width - len(line)) // 2)
                self.stdscr.addstr(start_y + i, start_x, line, color | curses.A_BOLD)

        if start_y + len(art) + 2 < height:
            self.stdscr.addstr(start_y + len(art) + 2, (width - len(msg)) // 2, msg, color | curses.A_BOLD)
            
        if start_y + len(art) + 4 < height:
            self.stdscr.addstr(start_y + len(art) + 4, (width - 40) // 2, "Press 'q' to exit, 'r' to restart")
            
        self.stdscr.refresh()

    def render_pause_screen(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        msg = "PAUSED"
        sub_msg = "Press 'p' to Resume, 'r' to Restart, 'q' to Quit"
        
        self.stdscr.addstr(height // 2 - 1, (width - len(msg)) // 2, msg, curses.A_BOLD)
        self.stdscr.addstr(height // 2 + 1, (width - len(sub_msg)) // 2, sub_msg)
        
        self.stdscr.refresh()

    def render_inventory_menu(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        title = " INVENTORY (Select to Inspect) "
        self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.A_BOLD | curses.A_UNDERLINE)
        
        inventory = self.game_state.inventory
        if not inventory:
            msg = "Your inventory is empty."
            self.stdscr.addstr(height // 2, (width - len(msg)) // 2, msg)
            instr = "Press 'i' or 'ESC' to return."
            self.stdscr.addstr(height - 2, (width - len(instr)) // 2, instr)
            return

        start_y = 5
        for i, item in enumerate(inventory):
            prefix = "> " if i == self.inventory_selection_index else "  "
            style = curses.A_REVERSE if i == self.inventory_selection_index else curses.A_NORMAL
            self.stdscr.addstr(start_y + i, 4, f"{prefix}{item}", style)
            
        # Show details of selected item
        if 0 <= self.inventory_selection_index < len(inventory):
            selected_item = inventory[self.inventory_selection_index]
            details = ITEM_DETAILS.get(selected_item)
            
            detail_x = 40
            if details:
                # Description
                desc = details.get("desc", "No description.")
                self.stdscr.addstr(start_y, detail_x, "Description:", curses.A_BOLD)
                
                # Simple word wrap for description
                max_desc_width = width - detail_x - 2
                words = desc.split(' ')
                current_line = ""
                line_offset = 1
                
                for word in words:
                    if len(current_line) + len(word) + 1 <= max_desc_width:
                        current_line += word + " "
                    else:
                        self.stdscr.addstr(start_y + line_offset, detail_x, current_line)
                        current_line = word + " "
                        line_offset += 1
                if current_line:
                    self.stdscr.addstr(start_y + line_offset, detail_x, current_line)
                    line_offset += 1
                
                # Art
                art_start_y = start_y + line_offset + 1
                art = details.get("art")
                if art:
                    for j, line in enumerate(art):
                        if art_start_y + j < height:
                            self.stdscr.addstr(art_start_y + j, detail_x, line)
                            
                # Clue overlay on art
                clue = details.get("clue")
                if clue:
                    clue_y = art_start_y + clue['y']
                    clue_x = detail_x + clue['x']
                    if clue_y < height:
                        self.stdscr.addch(clue_y, clue_x, clue['char'], curses.color_pair(clue['color_pair']) | curses.A_BOLD)
            else:
                self.stdscr.addstr(start_y, detail_x, "No details available.")

        instr = "UP/DOWN to select, 'i' or 'ESC' to return."
        self.stdscr.addstr(height - 2, (width - len(instr)) // 2, instr)
        self.stdscr.refresh()

    def handle_inventory_input(self):
        key = self.stdscr.getch()
        inventory = self.game_state.inventory
        
        if key == ord('i') or key == 27: # i or ESC
            self.state = "GAME"
        elif key == curses.KEY_UP:
            self.inventory_selection_index = max(0, self.inventory_selection_index - 1)
        elif key == curses.KEY_DOWN:
            self.inventory_selection_index = min(len(inventory) - 1, self.inventory_selection_index + 1)
    
    def render_debug_password(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        msg = "ENTER DEBUG PASSWORD:"
        self.stdscr.addstr(height // 2 - 2, (width - len(msg)) // 2, msg, curses.A_BOLD)
        
        # Display buffer
        display_buffer = "*" * len(self.debug_buffer)
        self.stdscr.addstr(height // 2, (width - len(display_buffer)) // 2, display_buffer)
        
        instr = "Press ENTER to submit, ESC to cancel"
        self.stdscr.addstr(height // 2 + 2, (width - len(instr)) // 2, instr, curses.A_DIM)
        
        self.stdscr.refresh()

    def handle_debug_password_input(self):
        key = self.stdscr.getch()
        if key == -1:
            return
            
        if key == 10 or key == 13: # Enter
            if self.debug_buffer == "AbraCaDaBra":
                self.state = "DEBUG_SELECT"
                self.inventory_selection_index = 0 # Reuse for room selection
            else:
                self.state = "PAUSE" # Failed
        elif key == 27: # ESC
            self.state = "PAUSE"
        elif key == 8 or key == 127 or key == curses.KEY_BACKSPACE:
            self.debug_buffer = self.debug_buffer[:-1]
        elif 32 <= key <= 126:
            self.debug_buffer += chr(key)

    def render_debug_select(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        title = " DEBUG: SELECT ROOM "
        self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.A_BOLD | curses.A_REVERSE)
        
        start_y = 5
        for i, room in enumerate(rooms_list):
            prefix = "> " if i == self.inventory_selection_index else "  "
            style = curses.A_REVERSE if i == self.inventory_selection_index else curses.A_NORMAL
            line = f"{prefix}{i}: {room.name}"
            self.stdscr.addstr(start_y + i, (width - len(line)) // 2, line, style)
            
        instr = "UP/DOWN to select, ENTER to warp, ESC to cancel"
        self.stdscr.addstr(height - 2, (width - len(instr)) // 2, instr)
        self.stdscr.refresh()

    def handle_debug_select_input(self):
        key = self.stdscr.getch()
        
        if key == 27: # ESC
            self.state = "PAUSE"
        elif key == curses.KEY_UP:
            self.inventory_selection_index = max(0, self.inventory_selection_index - 1)
        elif key == curses.KEY_DOWN:
            self.inventory_selection_index = min(len(rooms_list) - 1, self.inventory_selection_index + 1)
        elif key == 10 or key == 13: # Enter
            # Warp
            self.game_state.current_room_index = self.inventory_selection_index
            self.current_room = rooms_list[self.game_state.current_room_index]
            self.player_x = 1
            self.player_y = 1
            self.state = "GAME"
