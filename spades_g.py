import random
import os
import copy
import time

# -------------------------
# Spade 2-4-6: Sokoban
# -------------------------
class Spade_SB:
    def __init__(self, level):
        self.level = level
        self.grid, self.player_pos = self.generate_level(level)
        self.original_grid = copy.deepcopy(self.grid)

    def generate_level(self, level):
        wall = '■'
        space = ' '
        if level == 2:
            grid = [
                [wall, wall, wall, wall, wall],
                [wall, space, space, 'X', wall],
                [wall, space, 'B', space, wall],
                [wall, space, 'P', space, wall],
                [wall, wall, wall, wall, wall]
            ]
            player_pos = (3, 2)
        elif level == 4:
            grid = [
                [wall]*6,
                [wall, space, space, 'X', space, wall],
                [wall, space, 'B', wall, space, wall],
                [wall, space, space, 'B', space, wall],
                [wall, 'P', space, 'X', space, wall],
                [wall]*6
            ]
            player_pos = (4, 1)
        elif level == 6:
            grid = [
                [wall]*7,
                [wall, space, 'B', space, 'X', space, wall],
                [wall, space, space, space, wall, space, wall],
                [wall, space, wall, 'B', space, space, wall],
                [wall, space, space, space, 'X', 'B', wall],
                [wall, space, 'X', space, space, 'P', wall],
                [wall]*7
            ]
            player_pos = (5, 5)
        else:
            raise ValueError("Invalid difficulty level.")
        return grid, player_pos

    def display(self):
        print("\n♠ Spade Game - Sokoban")
        print("=" * 50)
        print("\nMap Info:")
        print("P: Player     B: Box")
        print("T: Target     #: Wall")
        print("=" * 50)
        for row in self.grid:
            print(' '.join(row))
        print()

    def move(self, direction):
        dx, dy = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}.get(direction, (0, 0))
        x, y = self.player_pos
        nx, ny = x + dx, y + dy
        nnx, nny = x + 2*dx, y + 2*dy

        def in_bounds(x, y):
            return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

        if not in_bounds(nx, ny):
            return

        target = self.grid[nx][ny]
        beyond = self.grid[nnx][nny] if in_bounds(nnx, nny) else '■'

        if target in [' ', 'X']:
            self.grid[x][y] = 'X' if self.original_grid[x][y] == 'X' else ' '
            self.grid[nx][ny] = 'P'
            self.player_pos = (nx, ny)

        elif target == 'B' and beyond in [' ', 'X']:
            self.grid[x][y] = 'X' if self.original_grid[x][y] == 'X' else ' '
            self.grid[nx][ny] = 'P'
            self.grid[nnx][nny] = 'B'
            self.player_pos = (nx, ny)
        elif target == 'B' and beyond not in [' ', 'X']:
            print("❌ You can't move the box there!")
            return False

    def check_win(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.original_grid[i][j] == 'X' and self.grid[i][j] != 'B':
                    return False
        return True

    def play(self):
        while True:
            self.display()
            if self.check_win():
                print("🎉 You won!")
                return True
            command = input("Move (w/a/s/d): ").lower()
            if command in ['w', 'a', 's', 'd']:
                if self.move(command) == False:
                    print("💀 Game Over! You can't move the box.")
                    return False
            else:
                print("Invalid command.")

    def clear_screen(self):
        time.sleep(3)  # Wait 3 seconds for the card visual to appear
        os.system('cls' if os.name == 'nt' else 'clear')

# -------------------------
# Spade 1-3-5: Lights Out
# -------------------------
class Spade_LO:
    def __init__(self, level):
        self.level = level
        self.lights = [random.choice([True, False]) for _ in range(3)]
        self.buttons = {
            0: [0, 1],
            1: [1, 2],
            2: [0, 2]
        }
        # Determine the number of attempts based on card number
        if level == 1:
            self.steps = 7
        elif level == 3:
            self.steps = 6
        else:  # level == 5
            self.steps = 5
        # Color codes
        self.colors = {
            'blue': '\033[94m',    # Blue
            'pink': '\033[95m',    # Pink
            'reset': '\033[0m'     # Reset color
        }

    def display(self):
        print(f"\n{self.colors['blue']}♠ Spade Game - Lights Out{self.colors['reset']}")
        
        print(f"{self.colors['pink']}Rules:")
        print("1. Click on a cell to toggle it and its adjacent cells")
        print(f"2. Try to turn off all lights{self.colors['reset']}")
        print("Lights:", ['💡' if l else '❌' for l in self.lights])
        print("Buttons: 0, 1, 2")
        print(f"Steps left: {self.steps}")

    def toggle(self, button):
        for i in self.buttons[button]:
            self.lights[i] = not self.lights[i]

    def start(self):
        while self.steps > 0:
            self.display()
            if not any(self.lights):
                print("🎉 All lights are off! You win!")
                return True
            try:
                choice = int(input("Press button (0-2): "))
                if choice in self.buttons:
                    self.toggle(choice)
                    self.steps -= 1
                else:
                    print("Invalid button.")
            except:
                print("Invalid input.")
        self.display()
        if not any(self.lights):
            print("🎉 You did it at the last step!")
            return True
        else:
            print("☠️ You failed to turn off all lights.")
            return False

    def clear_screen(self):
        time.sleep(3)  # Wait 3 seconds for the card visual to appear
        os.system('cls' if os.name == 'nt' else 'clear')

# -------------------------
# Game Handler
# -------------------------
def play_spades_game(card_number):
    if card_number in [2, 4, 6]:
        game = Spade_SB(card_number)
        return game.play()
    elif card_number in [1, 3, 5]:
        game = Spade_LO(card_number)
        return game.start()
    else:
        print("Invalid Spade card number!")
        return False
