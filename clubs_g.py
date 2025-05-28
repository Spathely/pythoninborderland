import random
import time

class Club_RPS:
    def __init__(self, card_number):
        self.card_number = card_number
        # For cards 2,4,6: goals are 3,2,1 respectively
        self.goal = 4 - (card_number // 2) if card_number % 2 == 0 else 7 - card_number
        self.choices = ["rock", "paper", "scissors"]
        self.colors = {
            'rules': '\033[95m',    # Pink
            'correct': '\033[92m',   # Green
            'wrong': '\033[91m',     # Red
            'reset': '\033[0m'       # Reset color
        }

    def get_computer_choice(self, player_history):
        if not player_history:
            return random.choice(self.choices)
        
        # Analyze the last 3 moves
        recent_moves = player_history[-3:]
        if len(recent_moves) >= 2:
            # If the player made the same move twice, choose the move that beats it
            if recent_moves[-1] == recent_moves[-2]:
                if recent_moves[-1] == 'rock':
                    return 'paper'
                elif recent_moves[-1] == 'paper':
                    return 'scissors'
                else:
                    return 'rock'
        
        return random.choice(self.choices)

    def determine_winner(self, player, computer):
        if player == computer:
            return "tie"
        elif (player == 'rock' and computer == 'scissors') or \
             (player == 'paper' and computer == 'rock') or \
             (player == 'scissors' and computer == 'paper'):
            return "player"
        else:
            return "computer"

    def play(self):
        print("\n♣ Club Card - Rock Paper Scissors")
        print(f"{self.colors['rules']}You need to win {self.goal} rounds to collect this card!{self.colors['reset']}")
        player_score = 0
        computer_score = 0

        while player_score < self.goal and computer_score < self.goal:
            player = input("Choose 'Rock', 'Paper' or 'Scissors': ").lower()
            if player not in self.choices:
                print("Invalid input.")
                continue
            computer = random.choice(self.choices)
            print(f"Other player: {computer}")
            if player == computer: #All possibilities during the round
                print("Draw.")
            elif (player == "rock" and computer == "scissors") or \
                 (player == "paper" and computer == "rock") or \
                 (player == "scissors" and computer == "paper"):
                player_score += 1
                print(f"{self.colors['correct']}You win this round!{self.colors['reset']}")
            else:
                computer_score += 1
                print(f"{self.colors['wrong']}Other player wins this round.{self.colors['reset']}")

            print(f"SCORE: You {player_score}/{self.goal} - Other Player {computer_score}/{self.goal}")

        return player_score > computer_score

class Club_CBG:
    def __init__(self, card_number):
        self.card_number = card_number
        self.code_length = {2: 3, 4: 4, 6: 5}[card_number]
        self.max_attempts = self.code_length + 1
        self.secret_code = self.generate_code()
        # ANSI color codes
        self.colors = {
            "correct": '\033[92m',    # Green
            "wrong_pos": '\033[94m',  # Blue
            "wrong": '\033[91m',      # Red
            "reset": '\033[0m',       # Reset color
            "rules": '\033[95m'       # Pink
        }

    def generate_code(self):
        digits = list(range(10))
        random.shuffle(digits)
        return digits[:self.code_length]

    def get_feedback(self, guess):
        feedback = []
        for i in range(self.code_length):
            if guess[i] == self.secret_code[i]:
                feedback.append(f"{self.colors['correct']}✓{self.colors['reset']}")
            elif guess[i] in self.secret_code:
                feedback.append(f"{self.colors['wrong_pos']}~{self.colors['reset']}")
            else:
                feedback.append(f"{self.colors['wrong']}✗{self.colors['reset']}")
        return " ".join(feedback)

    def play(self):
        print("\n♣ Club Card - Code Breaker")
        print(f"{self.colors['rules']}Try to break the {self.code_length}-digit secret code.")
        print(f"You have {self.max_attempts} attempts.")
        print(f"Hints: {self.colors['correct']}✓{self.colors['reset']} correct position | {self.colors['wrong_pos']}~{self.colors['reset']} wrong position but correct digit | {self.colors['wrong']}✗{self.colors['reset']} not in code{self.colors['reset']}")

        attempts = 0
        while attempts < self.max_attempts:
            try:
                raw = input(f"Guess {attempts+1}: ").strip()
                guess = [int(d) for d in raw]
                if len(guess) != self.code_length:
                    print(f"Enter a {self.code_length}-digit number.")
                    continue
                feedback = self.get_feedback(guess)
                print("Hint:", feedback)
                attempts += 1
                if guess == self.secret_code:
                    print(f"{self.colors['correct']}🎉 Correct code! You opened the door.{self.colors['reset']}")
                    return True
            except ValueError:
                print("Use only digits.")
        print(f"{self.colors['wrong']}💀 Code not broken. The code was: {''.join(map(str, self.secret_code))}{self.colors['reset']}")
        return False 
    

def play_club_game(card_number):
    if card_number in [1, 3, 5]:
        game = Club_RPS(card_number)
    elif card_number in [2, 4, 6]:
        game = Club_CBG(card_number)
    else:
        print("Invalid Spade card.")
        return False
    return game.play()
