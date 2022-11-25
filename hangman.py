# author: Anya Zhang
# date: 10/6/22
""" file: hangman.py is a program that will generate a dictionary word 
and ask the user to guess the word one letter at a time. 
The user will have a number of lives that will be set up in the beginning of the game. 
After the user uses all lives or guesses the word correctly, the programs will ask the user to play again.  """
# input: file 'dictionary.txt'
# output: prints hangman game

import random
dictionary_file = "dictionary.txt"   # make a dictionary.txt in the same folder where hangman.py is located

""" make a dictionary from a dictionary file ('dictionary.txt', see above)
dictionary keys are word sizes (1, 2, 3, 4, …, 12), and values are lists of words
for example, dictionary = { 2 : ['Ms', 'ad'], 3 : ['cat', 'dog', 'sun'] }
if a word has the size more than 12 letters, put it into the list with the key equal to 12 """
def import_dictionary (filename) :
    dictionary = {}
    max_size = 12
    for num in range(2, max_size + 1):
        dictionary[num] = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                word = line.rstrip('\n')
                word_len = len(word)
                if word_len >= 12:
                    dictionary[12].append(word)
                else:
                    dictionary[word_len].append(word)
    except FileNotFoundError:
        print("Oh no! The file does not exist!")
        
    return dictionary


# print the dictionary (use only for debugging)
def print_dictionary (dictionary) :
    max_size = 12
    for size, words in dictionary.items():
        print(size, ':', words)


# get options size and lives from the user, use try-except statements for wrong input
def get_game_options () :
    try:
        size = int(input("Please choose a size of a word to be guessed [3 - 12, default any size]:\n"))
        if size >= 3 and size <= 12:
            print("The word size is set to " + str(size) + '.')
        else:
            print("A dictionary word of any size will be chosen.")
            size = random.randint(3, 12)
    except ValueError:
        print("A dictionary word of any size will be chosen.")
        size = random.randint(3, 12)

    try:
        lives = int(input("Please choose a number of lives [1 - 10, default 5]:\n"))
        if lives >= 1 and lives <= 10:
            print("You have", lives, "lives.")
        else:
            print("You have 5 lives.")
            lives = 5            
    except ValueError:
        print("You have 5 lives.")
        lives = 5

    return (size, lives)


# plays the hangman game 
def play () :
    # print a game introduction
    print("Welcome to the Hangman Game!")

    # START MAIN LOOP (OUTER PROGRAM LOOP)
    play = True
    while play:
        """ set up game options (the word size and number of lives)
        select a word from a dictionary (according to the game options)
        use choice() function that selects an item from a list randomly, for example:
        mylist = ['apple', 'banana', 'orange', 'strawberry']
        word = choice(mylist) """
        game_options = get_game_options()
        size = game_options[0]
        lives = game_options[1]
        word_list = dictionary[size]
        hidden_word = random.choice(word_list).upper() 
        word = []
        for l in hidden_word:
            word.append(l)

        display = ["__"] * len(word)
        #if there is a hyphen in the hidden word
        if '-' in hidden_word:
            i = hidden_word.index('-')
            display[i] = '-'
        lives_indicator = 'O' * lives
        lives_idx = 0
        letters = []

        # START GAME LOOP   (INNER PROGRAM LOOP)
        ended = False
        while not ended:
            """ format and print the game interface:
            Letters chosen: E, S, P                list of chosen letters
            __ P P __ E    lives: 4   XOOOO        hidden word and lives """
            print("Letters chosen:", ", ".join(letters))
            print("  ".join(display) + "   lives: " + str(lives) + " " + lives_indicator)

            # END GAME LOOP   (INNER PROGRAM LOOP)
            """ check if the user guesses the word correctly or lost all lives,
            if yes finish the game """
            if word == display:
                print("Congratulations!!! You won! The word is " + hidden_word + '!')
                ended = True
                break
            elif lives == 0:
                print("You lost! The word is " + hidden_word + '!')
                ended = True
                break

            # ask the user to guess a letter
            guess_input = input("Please choose a new letter >\n")
            guess = guess_letter(guess_input, letters)

            # update the list of chosen letters
            letters.append(guess)

            """ if the letter is correct update the hidden word,
            else update the number of lives
            and print interactive messages   """
            if guess in word or guess.lower() in word:
                print("You guessed right!")
                for i in range(len(word)):
                    if word[i] == guess or word[i] == guess.lower():
                        display[i] = word[i]
            else:
                print("You guessed wrong, you lost one life.")
                lives -= 1
                lives_indicator = lives_indicator[0:lives_idx] + "X" + lives_indicator[lives_idx + 1:]
                lives_idx += 1

        # END MAIN LOOP (OUTER PROGRAM LOOP)
        play_input = input("Would you like to play again [Y/N]?\n")
        play = play_again(play_input)
        if not play:
            return


# ask the user to guess a letter
def guess_letter (guess_input, letters):
    try: 
        while True:
            while guess_input.upper() in letters:
                print("You have already chosen this letter.")
                guess_input = input("Please choose a new letter >\n")
            if guess_input.isalpha() and len(guess_input) == 1:
                return guess_input.upper()
            # guess is not a letter
            guess_input = input("Please choose a new letter >\n")
    except:
        guess_input = input("Please choose a new letter >\n")
        guess_letter(guess_input, letters)


""" ask if the user wants to continue playing, 
if yes start a new game, otherwise terminate the program """
def play_again ( input ) :
    if input != 'Y' and input != 'y':
        print("Goodbye!")
        return False
    else:
        return True



# MAIN
if __name__ == '__main__' :

    # make a dictionary from a dictionary file
    dictionary = import_dictionary(dictionary_file)

    play()