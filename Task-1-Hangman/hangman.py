
import random
import os

# ASCII gallows stages for 0 to 6 incorrect guesses
HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    ========
    """
]


def load_words(filename="English word.txt"):
    """Load valid words from the provided text file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = [
                line.strip().lower()
                for line in file
                if line.strip().isalpha()
                and len(line.strip()) >= 3
            ]

        if not words:
            raise ValueError("The word list is empty.")

        return words

    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
        print("Keep the word list in the same folder as hangman.py.")
        raise SystemExit


def display_game(secret_word, guessed_letters, mistakes):
    """Display the gallows, masked word, and guessed letters."""
    print(HANGMAN_STAGES[mistakes])

    masked_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

    print("Word:", masked_word)
    print("Incorrect guesses:", mistakes, "/ 6")
    print("Guessed letters:",
          " ".join(sorted(guessed_letters)) if guessed_letters
          else "None")


def play_hangman():
    """Run one complete Hangman game."""
    words = load_words()
    secret_word = random.choice(words)

    guessed_letters = set()
    mistakes = 0
    max_mistakes = 6

    print("=" * 35)
    print("      HANGMAN WORD GUESSING GAME")
    print("=" * 35)
    print("Guess the hidden word one letter at a time.")
    print("You have 6 incorrect guesses. Good luck!")

    while mistakes < max_mistakes:
        display_game(secret_word, guessed_letters, mistakes)

        if all(letter in guessed_letters for letter in secret_word):
            print("\nCongratulations! You guessed the word!")
            print("Secret word:", secret_word.upper())
            print("You win!")
            return

        guess = input("\nEnter a letter (or type quit): ").strip().lower()

        if guess == "quit":
            print("\nGame ended by the player.")
            print("The secret word was:", secret_word.upper())
            return

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Enter one alphabet letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. No penalty!")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!")
        else:
            mistakes += 1
            print("Incorrect guess! One attempt lost.")

    display_game(secret_word, guessed_letters, mistakes)
    print("\nGAME OVER! You have used all 6 incorrect guesses.")
    print("The secret word was:", secret_word.upper())
    print("Better luck next time!")


if __name__ == "__main__":
    while True:
        play_hangman()

        again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thank you for playing Hangman!")
            break

        print("\n" + "-" * 35 + "\n")
