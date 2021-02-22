#!/usr/bin/env python3
import random
import string
from time import sleep

from colorama import Back, Fore, Style

WORDLIST_FILENAME_EN = "words.txt"
WORDLIST_FILENAME_FR = "words_fr.txt"


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """

    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    word_discovery_progress = ["_ "] * len(secret_word)

    for index, letter in enumerate(secret_word):

        if letter in letters_guessed:
            word_discovery_progress[index] = letter

    return "".join(word_discovery_progress)


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    availabe_letters = []

    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            availabe_letters.append(letter)

    return " ".join(availabe_letters)


def update_nb_guesses(warnings, guesses):
    """
    warnings: int (of remaining warnings)
    guesses: int (of remaining guesses)
    Takes the value of warnings and subtracts 1, print the remaining warnings message
    If warnings <= 0, subtracts 1 to guesses and print a warning message
    returns warnings and nb_guesses
    """
    if warnings <= 0:
        print("You have no warnings left, now you loose a guess, you were warned !")
        guesses -= 1
    else:
        warnings -= 1
        print(f"You have {warnings} warnings left")

    return warnings, guesses


def is_guess_valid(user_guess, letters_guessed):
    # Check 1 : the user should only enter one letter
    if len(user_guess) != 1:
        print(f"WARNING : Please enter only one letter at a time")
        return False

    # Check 2 : the user should only enter letters from the alphabet or * if he needs a hint
    if user_guess not in string.ascii_lowercase and user_guess != '*':
        print(f"WARNING : Please enter a letter")
        return False

    # Check 3 : the user should not enter the same letter twice
    if user_guess in letters_guessed:
        print(f"WARNING : You have already tried this letter, please enter another one !")
        return False

    return True


def match_with_gaps(my_word, other_word, letters_guessed):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    if len(my_word) != len(other_word):
        return False

    count = 0
    for index, value in enumerate(other_word):
        if my_word[index] == value or my_word[index] == "_" and value not in letters_guessed:
            count += 1

    if count == len(other_word):
        return True

    return False


def show_possible_matches(my_word, letters_guessed, nb_guesses):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
    """
    if len(my_word.strip("_")) == 0:
        print("Come on ! Try to guess at least one letter, you can do it!")
        return nb_guesses

    # If their is only half of the word left to guess, we do not give hints anymore
    if len(my_word.strip("_")) >= len(my_word.strip(str(letters_guessed))):
        print("Seriously ? You are almost done, I can not help you now (You loose a guess, you tried to play it easy)")
        nb_guesses -= 1
        return nb_guesses

    # if the user uses the hint, he looses 3 guesses, confirm first
    confirm = input("CAREFUL, using the hint will make you loose 3 guesses, is this ok ? (y/n): ")
    if confirm == 'y':
        nb_guesses -= 3
        matches = []
        for word in wordlist:
            if match_with_gaps(my_word, word, letters_guessed):
                matches.append(word)

        if len(matches) == 0:
            print("No matching found.")

        print(" ".join(matches))
        return nb_guesses
    elif confirm == 'n':
        print("Alright !")
        return nb_guesses
    else:
        print("I said 'y' or 'n' please")


def load_words():
    """
    Ask the user what game version to start
    Select the corresponding word list
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    while True:
        game_version = int(input(
            "Please choose a version \n "
            "1- English words \n "
            "2- French words \n "
            "What version would you like (1 or 2)? : "))
        # 1 = English version
        if game_version == 1:
            with open(WORDLIST_FILENAME_EN, "r") as inFile:
                # line: string
                line = inFile.readline()
                # wordlist: list of strings
                return line.split()
        # 2 = French version
        elif game_version == 2:
            with open(WORDLIST_FILENAME_FR, "r") as inFile:
                # line: string
                line = inFile.readline()
                # wordlist: list of strings
                return line.split()
        else:
            print("Only 1 or 2 please")


def play_again():
    """
    Asks if the user wants to play again
    If yes, restart a game
    if no, returns False
    if else, asks again until 'y' or 'n'
    """
    while True:
        play_again = input("Play again ? (y/n): ").lower().strip()
        if play_again == "y":
            hangman(choose_word(wordlist))
        elif play_again == "n":
            print("Goodbye! This was fun.")
            return False
        else:
            print("Only 'y' or 'n' please")


def loose():
    """
    Print the game over message
    Ask the user if play again
    return False if user choose not to play again
    """
    print("Sorry, you ran out of guesses")
    print(f"The word was: {secret_word}")

    # Asks if the user wants to play again
    do_we_play_again = play_again()
    if not do_we_play_again:
        return False

    return True


def hangman(secret_word):
    """
    secret_word : str, which is a word from the word_list

    Start the hangman game
    """
    # Initial parameters
    nb_guesses = 15
    nb_tries = 0
    warnings = 3
    letters_guessed = []

    print("\t Welcome to the game Hangman!")
    # Asks the user to choose game mode, either hangman with hint or hangman without hint

    print(Fore.RED + "RULE : If you need a hint, you can enter * and I will gladly help you. However, "
                     "please be careful, you will loose 3 guesses if you use the help")
    print(Style.RESET_ALL)

    # Game tips
    print(Fore.RED + "TIPS : please enter 'stop' if you want to exit the game \n")

    print(Fore.YELLOW + f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(Style.RESET_ALL)

    while nb_guesses:
        sleep(1)
        print(" ")
        print("*********************")

        # We get which letters in the secret word has been guesses so far
        guessed_word = get_guessed_word(secret_word, letters_guessed).strip()

        # Before each round, gives the user a reminder of remaining guesses and available letters
        print(f"Your progress so far: {guessed_word}")
        print(f"You have {nb_guesses} guesses left")
        print(f"Available letters : {get_available_letters(letters_guessed)}")

        # Asks the user to guess and adds the letter to the letters_guessed list
        user_guess = input("Please guess a letter:").lower().strip()

        # If user wants to exit the game
        if user_guess == "stop":
            print("Goodbye for now !")
            break

        # If the input is not valid, the loop ends here
        if not is_guess_valid(user_guess, letters_guessed):
            warnings, nb_guesses = update_nb_guesses(warnings, nb_guesses)
            continue

        # Adds the letter to the already tried letters (except if this is the hint)
        if user_guess != '*':
            letters_guessed.append(user_guess)
            nb_tries += 1

        # In case the user needs a hint, he looses 3 lives
        if user_guess == "*":
            nb_guesses = show_possible_matches(guessed_word.replace(" ", ""), letters_guessed, nb_guesses)

            if nb_guesses == 0:
                do_continue = loose()
                if not do_continue:
                    break

            continue

        # Check if the word was guessed, or if we should continue the game
        if is_word_guessed(secret_word, letters_guessed):
            print(Back.GREEN + f"Congratulations! You found the word {secret_word} !")
            print(Style.RESET_ALL)
            print(f"You won in {nb_tries} guesses")

            # Total score = guesses_remaining* number unique letters in secret_word
            total_score = nb_guesses * len(set(secret_word))
            print(f"Your score is {total_score}")

            # Asks if the user wants to play again
            do_we_play_again = play_again()
            if not do_we_play_again:
                break

        elif user_guess in secret_word:
            print(Fore.GREEN + "Good guess !")
            print(Style.RESET_ALL)
            continue

        else:
            print(Fore.RED + "Oops! That letter is not in my word")
            print(Style.RESET_ALL)
            # Withdraw one guess each round
            nb_guesses -= 1

        # If no guesses left, lost, the game ends
        if nb_guesses == 0:
            do_continue = loose()
            if not do_continue:
                break


if __name__ == "__main__":
    # Load words from the .txt, ask also the game version to load the correct word db
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    hangman(secret_word)

