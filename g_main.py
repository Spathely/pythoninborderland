import random
import sys
import json
import os
import time
from hearts_g import Heart_EDG, Heart_HM  # Games for Hearts card
from diamond_g import Diamond_NMG, Diamond_CGM  # Games for Diamond card
from spades_g import Spade_SB, Spade_LO # Games for Spades card
from clubs_g import Club_CBG, Club_RPS
# Later, diamond_g, spades_g, clubs_g etc. files can be added

def get_card_visual(card):
    """Returns ASCII art representation of a card"""
    # Color codes
    red = '\033[91m'  # Red
    black = '\033[30m'  # Black
    reset = '\033[0m'  # Reset color
    
    # Determine card color
    color = red if card.suit in ["♥", "♦"] else black
    
    # Format number
    display_number = str(card.number)
    if card.number == '1':
        display_number = "A"
    
    card_art = f"""
    {color}┌─────────┐
    │ {display_number:<2}      │
    │         │
    │    {card.suit}    │
    │         │
    │      {display_number:>2} │
    └─────────┘{reset}
    """
    return card_art

def print_welcome():
    welcome_text = """
🎴  𝗪 𝗘 𝗟 𝗖 𝗢 𝗠 𝗘  𝗧 𝗢  𝗕 𝗢 𝗥 𝗗 𝗘 𝗥 𝗟 𝗔 𝗡 𝗗 𝗦 ! 🎴
    """
    # Get terminal width (default 80 characters)
    terminal_width = 80
    
    # Center the title
    padding = (terminal_width - len(welcome_text.strip())) // 2
    print("\n" + " " * padding + welcome_text.strip())
    
    # Center menu options
    menu_items = ["New Game", "Load Game", "View Cards", "Exit"]
    print()
    for item in menu_items:
        padding = (terminal_width - len(item)) // 2
        print(" " * padding + item)
    print()

class Card:
    def __init__(self, suit, number):
        self.suit = suit  # "♥", "♦", "♣", "♠"
        self.number = number  # 1-6

    def __str__(self):
        return f"{self.suit} {self.number}"

    def to_dict(self):
        return {"suit": self.suit, "number": self.number}

    @classmethod
    def from_dict(cls, data):
        return cls(data["suit"], data["number"])

def save_game(deck, current_card_index):
    save_data = {
        "deck": [card.to_dict() for card in deck],
        "current_card_index": current_card_index
    }
    with open("save_game.json", "w") as f:
        json.dump(save_data, f)
    print("\n✅ Game saved!")

def load_game():
    try:
        with open("save_game.json", "r") as f:
            save_data = json.load(f)
        deck = [Card.from_dict(card_data) for card_data in save_data["deck"]]
        return deck, save_data["current_card_index"]
    except FileNotFoundError:
        print("\n❌ No saved game found!")
        return None, None

def view_cards():
    try:
        with open('save_game.json', 'r') as f:
            game_state = json.load(f)
        deck = [Card.from_dict(card_data) for card_data in game_state['deck']]
        current_card_index = game_state['current_card_index']
        
        print("\n📚 Your Cards:")
        print(f"Progress: {current_card_index}/{len(deck)} cards completed\n")
        
        print("Card List:")
        print("-" * 50)
        for i, card in enumerate(deck[:current_card_index], start=1):
            print(f"✓ Card {i}: {card.suit} {card.number}")
        print("-" * 50)
            
    except FileNotFoundError:
        print("\n❌ No saved game found!")
        print("Start a new game to collect cards!")

def get_card_number(card_number):
    if card_number == 'A':
        return 1
    return int(card_number)

def play_card(card):
    print(f"\nPlaying card: {card.suit} {card.number}")
    card_visual = get_card_visual(card)
    print(card_visual)
    time.sleep(3)  # Wait 3 seconds for the card visual to be displayed
    
    success = False
    if card.suit == "♥":
        if card.number in ['2', '4', '6']:
            game = Heart_EDG(get_card_number(card.number))
        elif card.number in ['A', '3', '5']:
            game = Heart_HM(get_card_number(card.number))
        else:
            print("Invalid Heart card number!")
            return False
        success = game.start()
    elif card.suit == "♦":
        if card.number in ['A', '3', '5']:
            game = Diamond_NMG(get_card_number(card.number))
        elif card.number in ['2', '4', '6']:
            game = Diamond_CGM(get_card_number(card.number))
        else:
            print("Invalid Diamond card number!")
            return False
        success = game.start()
    elif card.suit == "♠":
        if card.number in ['A', '3', '5']:
            game = Spade_LO(get_card_number(card.number))
            success = game.start()
        elif card.number in ['2', '4', '6']:
            game = Spade_SB(get_card_number(card.number))
            success = game.play()
        else:
            print("Invalid Spade card number!")
            return False
    elif card.suit == "♣":
        if card.number in ['1', '3', '5']:
            game = Club_RPS(get_card_number(card.number))
        elif card.number in ['2', '4', '6']:
            game = Club_CBG(get_card_number(card.number))
        else:
            print("Invalid Club card number!")
            return False
        success = game.play()
    else:
        print("Invalid card!")
        success = False
    return success

def main():
    while True:
        print_welcome()
        choice = input("Your choice (1-4): ").strip()
        
        if choice == "1":  # New Game
            suits = ['♥', '♦', '♣', '♠']
            numbers = ['A', '2', '3', '4', '5', '6']
            deck = [Card(suit, number) for suit in suits for number in numbers]
            random.shuffle(deck)
            current_card_index = 0
            
            print("\n🕹️ Game starts! There are 24 cards.")
            while current_card_index < len(deck):
                card = deck[current_card_index]
                success = play_card(card)
                
                if not success:
                    print("\n💀 You lost the game. Card: ", card)
                    print("🩸 You died.")
                    break
                
                current_card_index += 1
                if current_card_index < len(deck):
                    save_choice = input("\nDo you want to save the game? (Y/N): ").strip().upper()
                    if save_choice == "Y":
                        save_game(deck, current_card_index)
            
            if current_card_index == len(deck):
                print("\n🏆 You successfully passed all cards! You survived.")
            
        elif choice == "2":  # Load Game
            deck, current_card_index = load_game()
            if deck is None:
                continue
            
            print("\n🕹️ Game loaded! Remaining cards:", len(deck) - current_card_index)
            while current_card_index < len(deck):
                card = deck[current_card_index]
                success = play_card(card)
                
                if not success:
                    print("\n💀 You lost the game. Card: ", card)
                    print("🩸 You died. Simulation ended.")
                    break
                
                current_card_index += 1
                if current_card_index < len(deck):
                    save_choice = input("\nDo you want to save the game? (Y/N): ").strip().upper()
                    if save_choice == "Y":
                        save_game(deck, current_card_index)
            
            if current_card_index == len(deck):
                print("\n🏆 You successfully passed all cards! You survived.")
            
        elif choice == "3":  # View Cards
            view_cards()
            
        elif choice == "4":  # Exit
            print("\n👋 Goodbye!")
            sys.exit()
            
        else:
            print("\n❌ Invalid choice! Please enter a number between 1-4.")
        
        input("\nPress Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
