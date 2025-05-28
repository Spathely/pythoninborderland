import random
import time
import os
import msvcrt

# -----------------------------
# Custom Errors
# -----------------------------
class InvalidGuessError(Exception):
    pass

class TimeOutError(Exception):
    pass

# -----------------------------
# Word Banks
# -----------------------------
class HangmanWords:
    def __init__(self):
        self.words = {
            1: ["team", "final"],
            3: ["design", "project"],
            5: ["computer", "software"]
        }

    def get_word(self, difficulty):
        return random.choice(self.words[difficulty])

class EDGWords:
    def __init__(self):
        self.words = {
            2: ["code", "maze", "play", "data"],
            4: ["brain", "object", "random", "player"],
            6: ["function", "program", "simulate", "solution"]
        }

    def get_word(self, difficulty):
        return random.choice(self.words[difficulty])

# -----------------------------
# Hangman Game (♥ 1-3-5)
# -----------------------------
class Heart_HM:
    def __init__(self, difficulty):
        self.word_bank = HangmanWords()
        self.secret_word = self.word_bank.get_word(difficulty)
        self.guessed_letters = set()
        self.remaining_attempts = 6
        self.correct_letters = set(self.secret_word)
        self.hangman_states = [
            '''
                -----
                |   |
                    |
                    |
                    |
                    |
             =========''',
            '''
                -----
                |   |
                O   |
                    |
                    |
                    |
             =========''',
            '''
                -----
                |   |
                O   |
                |   |
                    |
                    |
             =========''',
            '''
                -----
                |   |
                O   |
               /|   |
                    |
                    |
             =========''',
            '''
                -----
                |   |
                O   |
               /|\  |
                    |
                    |
             =========''',
            '''
                -----
                |   |
                O   |
               /|\  |
               /    |
                    |
             =========''',
            '''
                -----
                |   |
                O   |
               /|\  |
               / \  |
                    |
             ========='''
        ]
        self.colors = {
            'blue': '\033[94m',    # Blue
            'correct': '\033[92m',   # Green
            'wrong': '\033[91m',     # Red
            'reset': '\033[0m'       # Reset color
        }

    def display_progress(self):
        return " ".join([char if char in self.guessed_letters else "_" for char in self.secret_word])

    def clear_screen(self):
        time.sleep(3)  # Wait 3 seconds for the card visual to appear
        os.system('cls' if os.name == 'nt' else 'clear')

    def guess(self, letter):
        if not letter.isalpha() or len(letter) != 1:
            raise InvalidGuessError("Please enter a single letter.")
        letter = letter.lower()
        if letter in self.guessed_letters:
            raise InvalidGuessError(f"You already tried the letter '{letter}'.")
        self.guessed_letters.add(letter)
        if letter not in self.secret_word:
            self.remaining_attempts -= 1

    def is_won(self):
        return self.correct_letters.issubset(self.guessed_letters)

    def is_lost(self):
        return self.remaining_attempts <= 0

    def start(self):
        while not self.is_won() and not self.is_lost():
            self.clear_screen()
            print(f"\n{self.colors['blue']}♥ Heart Game - Hangman{self.colors['reset']}")
            self.display()
            try:
                guess = input("\nEnter a letter: ")
                self.guess(guess)
            except InvalidGuessError as e:
                print("⚠️", e)
                time.sleep(1)

        if self.is_won():
            print(f"\n🎉 Congratulations! You guessed the word: {self.secret_word}")
            return True
        else:
            print(f"\n💀 You lost. The correct word was: {self.secret_word}")
            return False

    def display(self):
        print(self.hangman_states[6 - self.remaining_attempts])
        print("\nWord:", self.display_progress())
        print("Remaining attempts:", self.remaining_attempts)
        print("Tried letters:", " ".join(sorted(self.guessed_letters)))

# -----------------------------
# Encrypted Door Game (♥ 2-4-6)
# -----------------------------
class Heart_EDG:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.word_bank = EDGWords()
        self.colors = {
            'blue': '\033[94m',    # Blue
            'reset': '\033[0m'     # Reset color
        }

    def shuffle_word(self, word):
        scrambled = list(word)
        while True:
            random.shuffle(scrambled)
            if ''.join(scrambled) != word:
                break
        return ''.join(scrambled)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start(self):
        word = self.word_bank.get_word(self.difficulty)
        scrambled = self.shuffle_word(word)
        time_limit = 15

        print(f"\n{self.colors['blue']}♥ Heart Game - Encrypted Door{self.colors['reset']}")
        print(f"You have {time_limit} seconds to solve the word.")
        print("Press Enter to start...")
        input()

        # Show scrambled word after time starts
        print(f"\nScrambled word: {scrambled}")
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            remaining = max(0, time_limit - elapsed)
            
            # Only update the time
            print(f"\r⏰ Time remaining: {remaining:.1f} seconds", end="", flush=True)
            
            if remaining <= 0:
                print("\n⏰ Time's up!")
                return False
            
            # Check for input without blocking
            if msvcrt.kbhit():
                guess = input("\nYour guess: ").strip().lower()
                if guess == word:
                    print("\n✅ Correct! The door is now open.")
                    return True
                elif guess:
                    print(f"❌ Wrong! Try again.")
                    time.sleep(1)  # Short delay
                    # Update time after wrong guess
                    elapsed = time.time() - start_time
                    remaining = max(0, time_limit - elapsed)
                    if remaining <= 0:
                        print("\n⏰ Time's up!")
                        return False

# -----------------------------
# Heart Card Game Starter
# -----------------------------
def play_heart_game(card_no):
    if card_no in [1, 3, 5]:
        game = Heart_HM(card_no)
        return game.start()
    elif card_no in [2, 4, 6]:
        game = Heart_EDG(card_no)
        return game.start()
    else:
        print("Invalid Heart card number (must be 1-6).")
        return False
