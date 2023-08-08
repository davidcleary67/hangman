#!/usr/bin/python3

"""
Program:   hangman.py
Version:   1.0
Date:      7 Aug 2023
Author:    David Cleary
Licencing: Copyright 2023 SuniTAFE. All rights reserved.
"""

## Imports

from os import system, name
import random

## Global variables and constants

"""
Gallows elements for printing.
"f" --> gallows frame, always displayed
"p" --> hangman person, to be displayed as wrong guesses are made
"""
GALLOWS = [{"f":"   ","p":"_________"},   # Gallows elements for printing.
           {"f":"  |         ","p":"|"},  # "f" --> gallows frame, always
           {"f":"  |        ","p":" O"},  #         displayed
           {"f":"  |        ","p":" |"},  # "p" --> hangman person, to be
           {"f":"  |        ","p":"---"}, #         displayed as wrong guesses 
           {"f":"  |        ","p":" | "}, #         are made
           {"f":"  |        ","p":"/ \\"},
           {"f":"  |        ","p":""},
           {"f":"__|__      ","p":""}]
           
GALLOWSCOUNT = 9 # Number of gallows elements.

WORDFILE = "nouns.txt" # Text file of words to guess.

MAXGUESSES = 8 # Maximum number of guesses.

## Functions

def displayHeader():
    """
    Display the program name.
    """
    print("*** SuniTAFE - Hangman ***")
    
def displayGallows(count):
    """
    Display the gallows.
    
    Parameters:
        count (integer): Number of incorrect guesses made.
    """
    # Step through the list of gallows print elements.
    for c in range(GALLOWSCOUNT):
        # Print a gallows frame element.
        # Optionally print a person element based upon the number of incorrect 
        # guesses.
        print(GALLOWS[c]["f"] + (GALLOWS[c]["p"] if c < count else ""))
    
def displayGuesses(guesses):
    """
    Display all guessed letters.
    
    Parameters:
        guesses (list of characters): All letters guesses, both correct and 
                                      incorrect.
    """
    print("Guesses: " + " ".join(guesses))
   
def displayWord(word, guesses):
    """
    Display word showing all correctly guessed letters.
    
    Parameters:
        word (string): Word to guess.
        guesses (list of characters): All letters guesses, both correct and 
                                      incorrect.
                                      
    Returns:
        Count of correctly guessed letters (integer).
    """
    foundCount = 0
    print("Word: ", end="")
    # Step through all letters in word.
    # Display each letter correctly guessed and increment a count.
    # Display underscore for each letter not yet correctly guessed.
    for l in word:
        if l in guesses:
            foundCount += 1
            print(l, end = " ")
        else:
            print("_", end = " ")
    print()
    
    # Return the count of correctly guessed letters.
    return foundCount
    

def loadWords():
    """
    Load words to guess from a text file.
    
    Returns:
        List of words to guess (list of strings).
    """
    file = open(WORDFILE, "r")
    words = file.readlines()
    file.close()
    return words
   
def selectWord(words):
    """
    Select a word to guess from list.
    
    Parameters:
        words (string): List of words to guess.
                                      
    Returns:
        Randomly selected word to guess (string).
    """
    index = random.randint(0, len(words) - 1)
    word = words[index].upper().rstrip("\n")
    return word
    
def clearScreen():
    """
    Clear the screen.
    """
    # For windows.
    if name == 'nt':
        system('cls')
 
    # For everything else.
    else:
        system('clear')
        
def main():
    """
    Main function.
    Play the hangman game.
    A word is randomly selected from a list of 1000 common English nouns.
    The player repeatedly guesses letters in the word.
    Information displayed back to the user consists of:
    * A gallows that adds an additional element of the person handing for 
      each incorrectly guessed letter
    * A list of all letters guessed, both correct and incorrect
    * The word currently being guessed showing correctly guessed letters in 
      their correct positions and underscores for letters not yet guessed.
    If the player guessed all letters within the word prior to the hangman 
    being fully displayed, that is, with less than eight incorrect guesses,
    then the player wins and "Well done, you won!" is displayed, otherwise,
    the player lost and "Sorry, you lost!" is displayed.
    """
    # Load the list of words from a file. 
    words = loadWords()
  
    # New game loop.
    # Play the hangman game.  When the game finishes give the player the 
    # opportunity to play again.
    while True:
        
        # Initialise game variables.
        guesses = []
        guessCount = 0 
        youWon = False
        
        # Randomly select a word.
        word = selectWord(words)
    
        # Game loop.
        # Whilst game is not over, repeatedly display gallows, guesses and 
        # progress towards guessing the word.
        # Exit the main loop when either all letters in the word have been
        # guessed or the maximum number of incorrectly guesses, eight, has
        # occurred. 
        while True:
            
            # Display game information.
            clearScreen()
            displayHeader()
            displayGallows(guessCount)
            displayGuesses(guesses)
            foundCount = displayWord(word, guesses)
            
            # The player has won. All the letters in the word have been guessed.
            # Exit the main loop.
            if foundCount == len(word):
                youWon = True
                break
           
            # Input validation loop. 
            # Loop until the player enters a valid guess.
            # A valid guess is a single letter that has not been guessed 
            # previously.
            while True:
                
                # Get the player's guess.
                guess = input("Guess: ").upper()
                
                # Guesses must be single letters.
                if len(guess) != 1 or not guess.isalpha():
                    print("Invalid guess.  Guesses must be a single letter.")
                    
                # Guesses must not have been guessed previously.
                elif guess in guesses:
                    print("Invalid guess.  Letter already used.")
                else:
                    break
           
            # Appened the current guess to the list of all guesses.
            guesses.append(guess)
            guesses.sort()
            
            # Increment the number of guesses. 
            if not guess in word:
                guessCount += 1
                
                # The player has lost.  The maximum number of incorrect guesses
                # has been reached.
                # Exit the main loop.
                if guessCount == MAXGUESSES:
                    break
    
        # Display whether the player has won or lost.
        print("Well done, you won!" if youWon else ("Sorry, you lost!  The word was " + word))
        
        # Ask the player whether they want to play another game.
        playAgain = input("\nDo you want to play again (Y/N)? ").upper()
        if playAgain != "Y":
            break
        
    print("\nGoodbye!") 
    
## Call the main function.  
if __name__ == "__main__":
    main()