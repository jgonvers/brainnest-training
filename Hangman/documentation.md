# Hangman
## Imports
```
import os
import random
```
> Libraries used in the code.
***
## Global
```
MAX_LIVES = 6
```
> This global variable is used to set the lives of the user.
```
SRC_FOLDER = os.path.join(os.getcwd(),"src")
WORDS_FILE_PATH = os.path.join(SRC_FOLDER,"words.txt")
```
> These global variables point to the path of the folder "src" and to the path of the file containing the words that could be chosen for the game.
***
## Main function
```
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
```
### Function breakdown
```
total_lives = 6
```
> Number of lives the player has.
```
word = get_random_word()
letters_to_guess = set([letter for letter in word])
```
> Gets a random word from the "words.txt" file and separates it for letter to be found. E.g.: "example" -> ["e","x","a","m","p","l"]
```
while total_lives:
    print_current(word,letters_to_guess)
    print(f"You have {total_lives} guess(es) remaining.")

    guess = get_user_input()
```
> While the user still has lives, gives a prompt for the letter to be guessed.
```
if not guess:
    print("Invalid input.")
    continue
```
> If the guess was invalid, inform the user and restart the loop.
```
else:
    if guess in letters_to_guess:
        print(f"You've guessed the letter {guess}!")
        letters_to_guess.remove(guess)
```
> If the guess was valid and the letter guessed was in the word, informs the user and removes the letter from the "letters_to_guess" set.
```
else:
    total_lives -= 1
    print(f"The word does not contain the letter {guess}")
```
> If the guess was valid but incorrect, informs the user and decreases its lives.
```
if not letters_to_guess:
    print(f"Congratulations!\nYou've guessed correctly the hidden word: {word}.")
    break
```
> If there are no more letters to be found, congratulates the user and ends the game.
```
if letters_to_guess:
    print(f"Tough luck, the hidden word was: {word}")
```
> If the user's lives are over and there are still letters to be found, the user loses and the game is over.
***
## Random word function
```
def get_random_word():
    with open(WORDS_FILE_PATH,"r") as rf:
        lines = rf.readlines()
        random_word = random.choice(lines).strip()
        return random_word
```
> This function takes a random word from the "words.txt" file and returns it.
### Function breakdown
```
with open(WORDS_FILE_PATH,"r") as rf:
        lines = rf.readlines()
```
> Stores the lines of the file in the variable "lines".
```
random_word = random.choice(lines).strip()
return random_word
```
> Selects a random line and returns it.
***
## User input function
```
def get_user_input():
    inp = input("Guess a letter:\n")
    if not inp.isalpha() or len(inp) > 1:
        return False
    return inp
```
> This function gets the input from a user and returns it if the input is a letter.
### Function breakdown
```
inp = input("Guess a letter:\n")
    if not inp.isalpha() or len(inp) > 1:
        return False
```
> If the input is anything other than a single letter, returns False.
```
return inp
```
> Else, returns the input given.
***
## Print word function
```
def print_current(word,letters_to_guess):
    for letter in word:
        if letter not in letters_to_guess:
            print(letter,end=" ")
        else:
            print("_",end=" ")
    print()
```
> This function prints to the user the word that is being guessed. For any letter that has not been guessed yet, it prints the "_" symbol instead.
### Function breakdown
```
for letter in word:
    if letter not in letters_to_guess:
        print(letter,end=" ")
```
> Prints all the letters that have already been guessed
```
else:
    print("_",end=" ")
```
> Prints the "_" symbol for each letter to be guessed.
```
print()
```
> Prints a line for formatting purposes.