'''
The hangman game is a word guessing game where the player is given a word and has to guess the letters that make up the word. 
The player is given a certain number of tries (no more than 6 wrong guesses are allowed) to guess the correct letters before the game is over.
'''

# Output
'''
You have 6 tries left.                                                                                                                                           
Used letters:                                                                                                                                                    
Word: _ _ _ _                                                                                                                                                    
Guess a letter: a 

You have 6 tries left.                                                                                                                                           
Used letters: a                                                                                                                                                  
Word: _ a _ a                                                                                                                                                    
Guess a letter: j    

You have 6 tries left.                                                                                                                                           
Used letters: j a                                                                                                                                                
Word: j a _ a                                                                                                                                                    
Guess a letter: v                                                                                                                                                
You guessed the word java !
'''
import os, random

MAX_LIVES = 6
SRC_FOLDER = os.path.join(os.getcwd(),"src")
WORDS_FILE_PATH = os.path.join(SRC_FOLDER,"words.txt")

def get_random_word():
    with open(WORDS_FILE_PATH,"r") as rf:
        lines = rf.readlines()
        random_word = random.choice(lines).strip()
        return random_word

def get_user_input():
    inp = input("Guess a letter:\n")
    if not inp.isalpha() or len(inp) > 1:
        return False
    return inp

def print_current(word,letters_to_guess):
    for letter in word:
        if letter not in letters_to_guess:
            print(letter,end=" ")
        else:
            print("_",end=" ")
    print()

def main():
    total_lives = 6

    word = get_random_word()
    letters_to_guess = set([letter for letter in word])

    while total_lives:
        print_current(word,letters_to_guess)
        print(f"You have {total_lives} guess(es) remaining.")

        guess = get_user_input()
        if not guess:
            print("Invalid input.")
            continue
        else:
            if guess in letters_to_guess:
                print(f"You've guessed the letter {guess}!")
                letters_to_guess.remove(guess)
            else:
                total_lives -= 1
                print(f"The word does not contain the letter {guess}")
        if not letters_to_guess:
            print(f"Congratulations!\nYou've guessed correctly the hidden word: {word}.")
            break

    if letters_to_guess:
        print(f"Tough luck, the hidden word was: {word}")


main()