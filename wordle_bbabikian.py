"""
Wordle Game
Author: Blake Babikian
Date: 03/0322
Description: 5 letter word guess game

"""
import random
STATS_FILE = "stats.txt"
valid = False
tries = 0

f = open('fiveletters.txt', 'r') # Open the list of five-letter word txt file
words = (f.read()).split() # makes a python list of the txt file list

def evaluate(guess, word): # This function figures out which letters are in the right places

    result = "" # Setting Variable
    for i in range(5): # For loop to go through each word
        l = guess[i] # Setting Variable
        if l == word[i]: # For loop if statement where guessed letter is correct
            result += "["+l+"]" # Add up letters that are correct
        elif l in word: # For loop if statement where guessed letter is present
            result += "<"+l+">" # Add up letters that are present
        else: # For loop if statement where guessed letter is absent
            result += "("+l+")" # Add up letters that are absent
    return result # Return guessed word with annotated letters

def available(guess, alphabet): # This function keeps track of letters available to guess

    for i in guess: # Slices guess up into individual letters
        alphabet = alphabet.replace(i, "") # Deltete the letters in guess and in alphabet
    return alphabet # Return a list of letters not guessed


def read_stats_from_file(): # This function loads initial stats from file
    global cheat, games_won, games_played, current_streak, max_streak, guess_distribution # Variables

    f = open('stats.txt','r') # Open Stats txt file in read
    text = f.read() # Write stats file on python variable
    stats = text.split() # Split stats into indivdual stats
    cheat = stats[0] # Set global variable to equivalent stats python file
    games_won = stats[2] # Set global variable to equivalent stats python file
    games_played = stats[1] # Set global variable to equivalent stats python file
    current_streak = stats[3] # Set global variable to equivalent stats python file
    max_streak = stats[4] # Set global variable to equivalent stats python file
    guess_distribution = [0, 0, 0, 0, 0, 0] # Set global variable to equivalent stats python file
    guess_distribution[0] = stats[5] # Set global variable to equivalent stats python file
    guess_distribution[1] = stats[6] # Set global variable to equivalent stats python file
    guess_distribution[2] = stats[7] # Set global variable to equivalent stats python file
    guess_distribution[3] = stats[8] # Set global variable to equivalent stats python file
    guess_distribution[4] = stats[9] # Set global variable to equivalent stats python file
    guess_distribution[5] = stats[10] # Set global variable to equivalent stats python file


def write_stats_to_file(): # This function erases old and writes updated stats
    global cheat, games_won, games_played, current_streak, max_streak, guess_distribution # Variables

    g = open('stats.txt', 'w') # Open and erase Stats txt file in write
    g.write(str(cheat)) #write variable stats file
    g.write('\n') #next line in stats file
    g.write(str(games_played)) #write variable stats file
    g.write('\n') #next line in stats file
    g.write(str(games_won)) #write variable stats file
    g.write('\n') #next line in stats file
    g.write(str(current_streak)) #write variable stats file
    g.write('\n') #next line in stats file
    g.write(str(max_streak)) #write variable stats file
    g.write('\n') #next line in stats file
    for q in range(0,6): # For loop to go through and update guess distribution in stats file
        text = (int((guess_distribution[q]))) # Set variable as integer and index guess distribution
        g.write(str(text)) # Write variable as string to stats file
        g.write('\n') # Next line in stats file
    g.close() # Save and close updated stats file

def show_stats(): # this function displays the stats sheet
    global cheat, games_played,games_won,current_streak, max_streak,guess_distribution # Variables

    m = open('stats.txt','r') # Open Stats txt file in read
    print("=====     Your Stats     =====") # Print head
    print(f"{'Games Played:':<17}{games_played:}") # Print title and Variable
    print(f"{'Win %':<17}{(int(games_won)/int(games_played)*100):>2.0f}%") # Print title and Variable with math
    print(f"{'Current Streak:':<17}{int(current_streak):>2.0f}") # Print title and Variable
    print(f"{'Max Streak:':<17}{int(max_streak):>2.0f}") # Print title and Variable
    print("====  Guess Distribution  ====") # Print head
    for q in range(0,6): # For loop to display guess distribution
        print((q+1),'',"*" * int((guess_distribution[q]))) # Print number of guesses (1,6) and star equivalent to guess count
    print(f"\n{'Cheating:'}\t{cheat.lower()}\n") # Print cheat
    m.close() # Close stats file

def game(): # This function is the logic behind the game
    global games_played,games_won,current_streak, max_streak,guess_distribution # Variables

    valid = False # Set variable
    while not valid: # While loop to ensure cheat word question does not fault
        cheatQ = (input("Do you want to use the cheat word? [Y/N]: ")).upper() # Cheat word question input make upper
        if cheatQ == "Y": # If cheat word question is Y enter
            word = "actor" # Set variable
            valid = True # Set variable
        elif cheatQ == "N": # If cheat word question is N enter
            word = random.choice(words) # Set variable
            valid = True # Set variable
        else: # If cheat word question is Y or N enter
            print("Please put a Y for cheat or a N for random") # Error message cheat word question invalid input
        games_played = int(games_played)+1 # Set variable
    tries = 0 # Set variable
    while tries <= 6: # While loop to make game last 6 turns
        alphabet = "abcdefghijklmnopqrstuvwxyz" # Set variable
        valid = False # Set variable
        while not valid: # While loop to ensure five-letter input is valid
            guess = (input(f'\n{tries+1}\t{" Guess a five-letter word: "}')).lower() # Five-letter word guess
            if type(guess) != str or len(guess) != 5 or guess not in words: # If statement with five-letter word criteria enter if invalid
                print("Invalid Entry! It must be a five-letter word:") # Print erroe msg
                valid = False # Set variable
            else: # If statement with five-letter word criteria enter if valid
                print('\t',evaluate(guess,word),available(guess,alphabet)) # Call the evaluate and available function
                alphabet = available(guess, alphabet) # Update variable
                if guess == word: # If statement enter if word guessed right
                    print("You win!", '\n') # Print winning statement
                    games_won = int(games_won)+1 # Update variable
                    current_streak = int(current_streak)+1 # Update variable
                    if int(current_streak) > int(max_streak): # If statement enter if new max streak
                        max_streak = int(current_streak) # Update variable
                    guess_distribution[tries] = int(guess_distribution[tries])+1 # Update variable
                    tries = 7 # Exits game
                    break # Exits game
                elif guess != word: # If statement enter if word guessed wrong
                    tries += 1 # Adds tries after wrong guess
                    if tries == 6: # If statement enter if there have been 6 tries
                        print("Oops! The word was",word) # Prints losing msg
                        current_streak = 0 # Updates variable if lose
                        tries = 7 # Exits games
                        break # Exits game

def main(): # This function is the game
    print("====  Welcome to Wordle!  ====\n") # Print Head
    read_stats_from_file() # Call function
    show_stats() # Call function

    while True:
        game() # Call function
        print('\n') # Print Space
        play_again = input("Do you want to play again? [Y/N] ").upper() # Playagain? input  make uppercase
        while play_again not in 'YN': # While loop to ensure valid playagain? input
            play_again = input("Error. Do you want to play again? [Y/N] ").upper() # Playagainerror? input  make uppercase
        if play_again == 'N': # If statement enter if playagain? in no
            write_stats_to_file() # Call function
            break # Break

main() # Call function
