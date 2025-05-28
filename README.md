# Borderlands Card Gauntlet

Welcome to the Borderlands Card Gauntlet! This project is a collection of mini-games, each triggered by drawing a specific card from a standard 24-card deck (6 cards per suit, Ace to 6). The goal is to successfully complete the game associated with each drawn card to survive.

## 🃏 Game Overview

The game master (`g_main.py`) manages a shuffled deck of 24 cards. When a card is drawn, it triggers a specific mini-game based on its suit and number. If you win the mini-game, you draw the next card. If you lose, the game ends. Progress can be saved and loaded.

## 🎮 The Games

Each suit has two types of games, typically one for odd-numbered cards (Ace, 3, 5) and another for even-numbered cards (2, 4, 6). (Note: Ace is treated as 1 for game logic).

### ♥️ Hearts Games (`hearts_g.py`)

*   **Hangman (Ace, 3, 5):**
    *   Guess the secret word letter by letter before running out of attempts.
    *   Difficulty (word length/complexity) varies with the card number.
*   **Encrypted Door Game (2, 4, 6):**
    *   Unscramble a given word within a time limit.
    *   Word difficulty/length depends on the card number.

### ♦️ Diamonds Games (`diamond_g.py`)

*   **Number Memory (Ace, 3, 5):**
    *   Memorize a sequence of numbers shown briefly.
    *   Recall the numbers in the correct order after they disappear.
    *   The quantity of numbers increases with the card number.
*   **Color Grid Memory (2, 4, 6):**
    *   Memorize the positions of colored cells on a grid.
    *   After the colors disappear, recall their locations.
    *   Grid size increases with the card number.

### ♣️ Clubs Games (`clubs_g.py`)

*   **Rock Paper Scissors (Ace, 3, 5):** (Note: Ace is card number 1 for this game)
    *   Play Rock Paper Scissors against the computer.
    *   You need to win a specific number of rounds based on the card number.
*   **Code Breaker (2, 4, 6):**
    *   Guess a secret multi-digit code within a limited number of attempts.
    *   Feedback is given for correct digits in the correct or wrong positions.
    *   Code length increases with the card number.

### ♠️ Spades Games (`spades_g.py`)

*   **Lights Out (Ace, 3, 5):**
    *   A small grid of lights is presented, some on, some off.
    *   Pressing a button toggles its state and the state of adjacent lights.
    *   The goal is to turn all lights off within a limited number of steps.
    *   The number of allowed steps varies with the card number.
*   **Sokoban (2, 4, 6):**
    *   Push boxes ('B') onto target locations ('X') in a grid-based puzzle.
    *   The player ('P') cannot pull boxes or push more than one box at a time.
    *   Map complexity increases with the card number.

## 📂 File Structure

*   `g_main.py`: The main game engine, handles card deck, game flow, saving/loading, and calling suit-specific games.
*   `hearts_g.py`: Contains the logic for Heart card games (Hangman, Encrypted Door).
*   `diamond_g.py`: Contains the logic for Diamond card games (Number Memory, Color Grid Memory).
*   `clubs_g.py`: Contains the logic for Club card games (Rock Paper Scissors, Code Breaker).
*   `spades_g.py`: Contains the logic for Spade card games (Lights Out, Sokoban).
*   `save_game.json`: Stores saved game progress (if any).

## 🚀 How to Run

1.  Ensure you have Python 3 installed.
2.  Clone the repository or download the `.py` files into a single directory.
3.  Open a terminal or command prompt in that directory.
4.  Run the main game file using the command:
    ```bash
    python g_main.py
    ```
5.  Follow the on-screen prompts to start a new game, load a game, or view cards.

## ⚙️ Dependencies

The game uses standard Python libraries:
*   `random`
*   `time`
*   `os`
*   `msvcrt` (for non-blocking input in some games, primarily for Windows)
*   `json` (for saving/loading game state)
*   `sys`
*   `copy` (for deep copying game states, e.g., in Sokoban)

No external packages need to be installed if you have a standard Python installation. The game uses ANSI escape codes for colored text, which should work on most modern terminals.

---

Enjoy the challenge! 