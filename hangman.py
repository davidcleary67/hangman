#!/usr/bin/python3

"""
Program:   hangman.py
Version:   1.0
Date:      7 Aug 2023
Author:    David Cleary
Licencing: Copyright 2023 SuniTAFE. All rights reserved.
Platforms: AWS-Linux, Windows 11
"""

## Imports

from os import system, name
import random
import sys
import os
from datetime import datetime
from hangmancfg import WORDFILE, SCOREFILE, LOGFILE

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

MAXGUESSES = 8 # Maximum number of guesses.

## Functions

def displayHeader(score):
    """
    Display the program name.
    """
    successRate = round((score['w'] / score['g'] if score['g'] > 0 else 0) * 100)
    print(f"*** SuniTAFE - Hangman *** Success rate: {successRate}%")
    
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
    
def loadWords(wordFile):
    """
    Load words to guess from a text file.
    
    Returns:
        List of words to guess (list of strings).
    """
    file = open(wordFile, "r")
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
    
def loadScore():
    """
    Load score information from a text file.
    
    Returns:
        Score information (dictionary).
    """
    file = open(SCOREFILE, "r")
    scoreText = file.readline()
    score = {}
    score['g'] = int(scoreText.split()[0])
    score['w'] = int(scoreText.split()[1])
    file.close()
    return score
    
def saveScore(score):
    """
    Save score information to a text file.
    
    Parameters:
        score (dictionary): Score information.
    """
    file = open(SCOREFILE, "w")
    file.write(f"{score['g']} {score['w']}\n")
    file.close()

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
        
def writeLog(success, word, guesses):
    """
    Writes message to log file.
    
    Parameters:
        word (string): Word to guess.
        guesses (list of characters): All letters guesses, both correct and 
                                      incorrect.
    """
    file = open(LOGFILE, "a")
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file.write(f"{'SUCCESS' if success else 'FAILURE'} {dateTimeStamp} {word} {''.join(guesses)}\n")
    file.close()

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

    # Process the optional word file from the command line.
    success = False
    argCount = len(sys.argv)
    
    if argCount > 2:
        print("Usage: hangman.py [wordFile]")
    else:
        if argCount == 1:        
            wordFile = WORDFILE
            success = True
        elif argCount == 2:
            wordFile = sys.argv[1]
            if os.path.exists(wordFile):
                success = True
            else:
                print(f"Error: Word file {wordFile} does not exist.")

        if success:
            # Load the list of words from a file. 
            words = loadWords(wordFile)
            
            # Load the score information from a file.
            score = loadScore()
          
            # New game loop.
            # Play the hangman game.  When the game finishes give the player the 
            # opportunity to play again.
            while True:
                
                # Initialise game variables.
                guesses = []
                guessCount = 0 
                youWon = False
                score['g'] += 1
                
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
                    displayHeader(score)
                    displayGallows(guessCount)
                    displayGuesses(guesses)
                    foundCount = displayWord(word, guesses)
                    
                    # The player has won. All the letters in the word have been guessed.
                    # Exit the main loop.
                    if foundCount == len(word):
                        youWon = True
                        score['w'] += 1
                        writeLog(True, word, guesses)
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
                            writeLog(False, word, guesses)
                            break
            
                # Display whether the player has won or lost.
                print("Well done, you won!" if youWon else ("Sorry, you lost!  The word was " + word))
                
                # Ask the player whether they want to play another game.
                playAgain = input("\nDo you want to play again (Y/N)? ").upper()
                if playAgain != "Y":
                    break
                
            # Save the score information.
            saveScore(score)    
            
            print("\nGoodbye!") 

## Call the main function.  
if __name__ == "__main__":
    main()