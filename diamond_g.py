import random
import time
import os
import msvcrt

# -----------------------------
# Custom Errors
# -----------------------------
class InvalidExpressionError(Exception):
    pass

class TimeOutError(Exception):
    pass

class InvalidInputError(Exception):
    pass

# -----------------------------
# Number Memory Game (♦ 1-3-5)
# -----------------------------
class Diamond_NMG:
    def __init__(self, card_no):
        self.card_no = card_no
        self.numbers = []
        self.time_limit = 8  # 8 seconds for each level
        self.colors = {
            'blue': '\033[94m',    # Blue
            'correct': '\033[92m',   # Green
            'wrong': '\033[91m',     # Red
            'info': '\033[94m',      # Blue
            'reset': '\033[0m'       # Reset color
        }
        self.generate_numbers()

    def generate_numbers(self):
        if self.card_no == 1:
            self.numbers = random.sample(range(1, 10), 3)  # 3 numbers
        elif self.card_no == 3:
            self.numbers = random.sample(range(1, 10), 4)  # 4 numbers
        elif self.card_no == 5:
            self.numbers = random.sample(range(1, 10), 5)  # 5 numbers

    def clear_screen(self, delay=3):
        if delay > 0:
            time.sleep(delay)
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_numbers(self):
        self.clear_screen()
        print(f"\n{self.colors['blue']}♦ Diamond Game - Number Memory{self.colors['reset']}")
        print("\nPress Enter to start...")
        input()
        
        print(f"\n{self.colors['info']}Remember these numbers:{self.colors['reset']}")
        print(f"{self.colors['info']}{' '.join(map(str, self.numbers))}{self.colors['reset']}")
        print(f"\nYou have {self.time_limit} seconds to memorize...")
        
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            remaining = self.time_limit - (time.time() - start_time)
            print(f"\r⏰ Time remaining: {remaining:.1f} seconds", end="", flush=True)
            time.sleep(0.1)
        
        self.clear_screen(delay=0) # Clear screen immediately
        print(f"\n{self.colors['blue']}♦ Diamond Game - Number Memory{self.colors['reset']}")
        print(f"\n{self.colors['info']}Time\'s up! Enter the numbers in the correct order.{self.colors['reset']}")

    def get_user_input(self):
        try:
            user_input = input("\nEnter the numbers (space-separated): ").strip()
            user_numbers = [int(x) for x in user_input.split()]
            return user_numbers
        except ValueError:
            print(f"{self.colors['wrong']}Please enter valid numbers!{self.colors['reset']}")
            return None

    def check_answer(self, user_numbers):
        if user_numbers == self.numbers:
            print(f"\n{self.colors['correct']}✅ Correct! You remembered all numbers in the right order!{self.colors['reset']}")
            return True
        else:
            print(f"\n{self.colors['wrong']}❌ Wrong! The correct order was: {' '.join(map(str, self.numbers))}{self.colors['reset']}")
            return False

    def start(self):
        self.show_numbers()
        while True:
            user_numbers = self.get_user_input()
            if user_numbers is not None:
                if len(user_numbers) != len(self.numbers):
                    print(f"{self.colors['wrong']}Please enter exactly {len(self.numbers)} numbers!{self.colors['reset']}")
                    continue
                return self.check_answer(user_numbers)

# -----------------------------
# Color Grid Memory Game (♦ 2-4-6)
# -----------------------------
class Diamond_CGM:
    def __init__(self, card_number):
        self.card_number = card_number
        self.grid_size = {2: 3, 4: 4, 6: 5}[card_number]
        self.color_pool = ['RED', 'GREEN', 'BLUE']
        self.reveal_count = 3
        # ANSI color codes
        self.color_codes = {
            'RED': '\033[41m  \033[0m',    # Red background
            'GREEN': '\033[42m  \033[0m',  # Green background
            'BLUE': '\033[44m  \033[0m'    # Blue background
        }
        # Row and column labels based on grid size
        self.rows = ['A', 'B', 'C', 'D', 'E'][:self.grid_size]
        self.cols = ['1', '2', '3', '4', '5'][:self.grid_size]
        self.colors = {
            'blue': '\033[94m',    # Blue
            'correct': '\033[92m',   # Green
            'wrong': '\033[91m',     # Red
            'white': '\033[97m',     # White
            'reset': '\033[0m'       # Reset color
        }

    def clear_screen(self):
        time.sleep(3)  # Wait 3 seconds for the card visual to appear
        os.system('cls' if os.name == 'nt' else 'clear')

    def generate_color_grid(self):
        # Create a grid with one of each color
        grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        colors = self.color_pool.copy()
        random.shuffle(colors)
        
        # Place colors in random positions
        positions = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)]
        random.shuffle(positions)
        
        for color, (i, j) in zip(colors, positions[:3]):  # Place only in the first 3 positions
            grid[i][j] = color
            
        return grid

    def display_grid(self, grid, reveal=False):
        # Show column numbers
        print(f"{self.colors['white']}   " + "  ".join(self.cols))
        
        for i, row in enumerate(grid):
            # Show row letter
            print(f"{self.colors['white']}{self.rows[i]} ", end="")
            
            for cell in row:
                if reveal and cell in self.color_codes:
                    print(self.color_codes[cell], end=" ")
                else:
                    print(f"{self.colors['white']}■{self.colors['reset']}", end=" ")
            print()
        print(f"{self.colors['reset']}")

    def get_color_position(self, grid, color):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if grid[i][j] == color:
                    return f"{self.rows[i]}{self.cols[j]}"
        return None

    def validate_position(self, guess):
        # Clear spaces and convert to uppercase
        guess = guess.strip().upper()
        
        # If longer than 2 characters or empty, invalid
        if len(guess) != 2 or not guess:
            return False, "Please enter a 2-character position (e.g., A1 or 1A)"
            
        # First character can be a letter, second a number, or vice-versa
        if guess[0] in self.rows and guess[1] in self.cols:
            return True, f"{guess[0]}{guess[1]}"
        elif guess[0] in self.cols and guess[1] in self.rows:
            return True, f"{guess[1]}{guess[0]}"
        else:
            return False, f"Invalid position! Available letters: {', '.join(self.rows)}, Available numbers: {', '.join(self.cols)}"

    def start(self):
        print(f"\n{self.colors['blue']}♦ Diamond Game - Color Grid Memory{self.colors['reset']}")
        print(f"Grid Size: {self.grid_size}x{self.grid_size}")
        print("Remember the positions of the colors! Each color appears only once.")
        print(f"Positions are marked with letters ({self.rows[0]}-{self.rows[-1]}) and numbers ({self.cols[0]}-{self.cols[-1]}).")
        print(f"Example: A1 or 1A{self.colors['reset']}\n")
        
        grid = self.generate_color_grid()
        
        print("Showing the colored grid to remember...")
        self.display_grid(grid, reveal=True)
        time.sleep(5)
        self.clear_screen()

        print("Now answer where each color is located (e.g., A1 or 1A):\n")
        self.display_grid(grid)

        correct_answers = 0
        for color in self.color_pool:
            correct_pos = self.get_color_position(grid, color)
            while True:
                guess = input(f"Where is {color}? ").strip()
                is_valid, result = self.validate_position(guess)
                
                if is_valid:
                    if result == correct_pos:
                        print(f"{self.colors['correct']}✓ Correct!{self.colors['reset']}")
                        correct_answers += 1
                    else:
                        print(f"{self.colors['wrong']}✗ Wrong! {color} was at {correct_pos}{self.colors['reset']}")
                    break
                else:
                    print(f"⚠️ {result}")
                    print("Please try again.")

        if correct_answers == len(self.color_pool):
            print(f"\n{self.colors['correct']}🎉 Perfect! You remembered all colors correctly!{self.colors['reset']}")
            return True
        else:
            print(f"\n{self.colors['wrong']}❌ You got {correct_answers} out of {len(self.color_pool)} correct.{self.colors['reset']}")
            return False

# -----------------------------
# Game Runner
# -----------------------------
def play_diamond_game(card_no):
    if card_no in [1, 3, 5]:
        game = Diamond_NMG(card_no)
        return game.start()
    elif card_no in [2, 4, 6]:
        game = Diamond_CGM(card_no)
        return game.start()
    else:
        print("Invalid Diamond card number (must be 1-6).")
        return False
