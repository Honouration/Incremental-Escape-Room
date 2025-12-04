import curses
import sys
import os

# Add src to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.gamestate import GameState
from src.engine import GameEngine

def main(stdscr):
    game_state = GameState()
    engine = GameEngine(stdscr, game_state)
    engine.run()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except ImportError:
        print("Error: 'windows-curses' is not installed.")
        print("Please run: pip install -r requirements.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
