#LIBRARY CALLS:

import hashlib
import random
import base64
import os
import re
import string
from cryptography.fernet import Fernet

#---------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------------------#

#FILE CHECKER:
#check files.

def ensure_file_exists(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            pass

#Wordlist creation and check
def generate_random_word(length = 8):
    return "".join(random.choice(string.ascii_lowercase) for _ in range (length))

def crete_random_wordlist(file_name, num_words=2048):
    with open(file_name, "w") as file:
        for _ in range(num_words):
            word = generate_random_word(random.randint(4, 8))
            file.write(word + "\n")
    print(f"Wordlist generated with {num_words} words.")


def ensure_wordlist_exist(file_name = "wordlist.txt"):
    if not os.path.exists(file_name):
        print(f"{file_name} not found.Generating a random wordlist ...")
        crete_random_wordlist(file_name)
    else:
        print(f"{file_name} already exists.")

#-----------------------------------------------------------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------------------------------------------------------#

#SEED PHRASE FUNCTIONS:

# Function to load the word list from a file
def load_word_list(wordlist):
    with open(f"{wordlist}.txt", "r") as file:
        # Read all lines from the file and strip newline character
        words = [line.strip() for line in file.readlines()]
    return words

# Function to generate a secure seed phrase (randomly generated)
def generate_seed_phrase(word_list, num_words=12):
    # Generate a random 12-word seed
    seed_phrase = " ".join(random.choice(word_list) for _ in range(num_words))
    print(f"Your generated seed phrase is: {seed_phrase}")
    return seed_phrase

# Get the seed phrase from the user
def get_user_seed_phrase():
    seed_phrase = input("Enter your unique seed phrase: ")
    return seed_phrase

# Hash the seed phrase
def hash_the_seed_phrase(seed_phrase):
    # Hashing seed phrase with sha256
    hashed_seed = hashlib.sha256(seed_phrase.encode()).hexdigest()
    return hashed_seed

def store_hashed_seed(hashed_seed):

    #Create if there isnt.
    if not os.path.exists("hashed_seed.txt"):
        with open("hashed_seed.txt","w") as file:
            file.write("")    

    with open("hashed_seed.txt", "w") as file:
        file.write(hashed_seed)
    print(f"Stored hashed seed: {hashed_seed}")  # For debugging


# Function to check if the entered seed matches the stored hash
def check_seed_phrase(entered_seed, max_attempts = 3):
    hashed_entered_seed = hash_the_seed_phrase(entered_seed)

    with open("hashed_seed.txt", "r") as file:
        stored_hash = file.read().strip()

        attempts = 0

        while attempts < max_attempts:
            if hashed_entered_seed == stored_hash:
                return True
            else:
                attempts += 1
                print(f"Incorrect seed phrase. Attempts remaining: {max_attempts - attempts}")
                
                if attempts < max_attempts:
                    entered_seed = input("Re-enter your seed phrase: ")
                    hashed_entered_seed = hash_the_seed_phrase(entered_seed)

    print("Too many failed attmepts. Exiting ...")
    return False

#---------------------------------------------------------------------------------------------------------------------------------------#


#---------------------------------------------------------------------------------------------------------------------------------------#

#PASSWORDS-ACCOUNTS-WEBSITE FUNCTIONS:

def get_user_account():
    account_name = input(f"Enter your account name:")
    return account_name


def get_user_identifier():
    identifier = input(f"Enter your account identifier:")
    return identifier
    

def get_user_password():
    while True:        
        password = input(f"Enter your password:")
        is_valid, message = validate_password_strenght(password)
        if is_valid:
            return password
        else: 
            print("Invalid password")
    

def validate_password_strenght(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, "Password is strong."
    



#HASHING & ENCRYPTION FUNCTIONS

#Hash identifier
def hash_user_identifier(identifier, seed_phrase):
    return hashlib.sha256((identifier + seed_phrase).encode()).hexdigest()

#Hash account
def hash_user_account(account, seed_phrase):
    return hashlib.sha256((account + seed_phrase).encode()).hexdigest()

#Hashh password
def hash_user_password(password, seed_phrase):
    return hashlib.sha256((password + seed_phrase).encode()).hexdigest()

#Encrypted key from seedphrase
def generate_encryption_key(seed_phrase):
    key = hashlib.sha256((seed_phrase.encode())).digest()[:32]
    return base64.urlsafe_b64encode(key)
    
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())
    pass

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

def store_encrypted_data(identifier, account, password, key):

    encrypted_identifier = encrypt_data(identifier, key)
    encrypted_account = encrypt_data(account, key)
    encrypted_password = encrypt_data(password, key)

    #Create if there isnt 
    if not os.path.exists("accounts.txt"):
        with open("accounts.txt","w") as file:
            file.write("")

    with open ("accounts.txt", "a") as file:
        file.write(f"{encrypted_identifier.decode()}|{encrypted_account.decode()}|{encrypted_password.decode()}\n")
    print("Account data stored securely.")
    
def retrieve_and_decrypt_data(key):
    try:
        with open("accounts.txt","r") as file:
            
            lines = file.readlines()

            accounts = []

            for line in lines:

                encrypted_identifier, encrypted_account, encrypted_password = line.strip().split("|")

                identifier = decrypt_data(encrypted_identifier.encode(), key)
                account = decrypt_data(encrypted_account.encode(), key)
                password = decrypt_data(encrypted_password.encode(), key)

                accounts.append((identifier, account, password))

            return accounts

    except FileNotFoundError:
        print("No accounts found")
        return []

#---------------------------------------------------------------------------------------------------------------------------------------#
       

#---------------------------------------------------------------------------------------------------------------------------------------#
def main():
    # Load the word list from the file (replace 'wordlist' with your actual wordlist file name)
    word_list = load_word_list("wordlist")
    
    # Ask user if they already have a seed phrase
    user_input = input("Do you have a seed phrase already? Press [y] if you have, [n] if you don't: ").strip().lower()
    
    #SEED GENERATOR
        #If user dont have a seedphrase: 
    if user_input == "n":

        # If no seed, generate one
        seed_phrase = generate_seed_phrase(word_list)
        # Store the generated seed in a secure place (for demo, we're storing the hashed version)
        hashed_seed = hash_the_seed_phrase(seed_phrase)
        store_hashed_seed(hashed_seed)
        print(f"Generated seed phrase: {seed_phrase}")
        print("Seed phrase stored securely!")


    #AUTHENTICATION
        #If user has a seed phrase: 
    elif user_input == "y":

        # If user already has a seed phrase, let them input it
        seed_phrase = get_user_seed_phrase()
        hashed_seed = hash_the_seed_phrase(seed_phrase)
        # 3. Login functionality (for the user to check if the seed matches)
                
        if check_seed_phrase(seed_phrase):
            print("Authentication successful!")
        else:
            print("Authentication failed. Exiting ...")
            return

        #ONCE AUTHENTICATED.
        running = True

        while running:

            #Checkers

            ensure_file_exists("hashed_seed.txt")
            ensure_file_exists("accounts.txt")
            ensure_wordlist_exist("wordlist.txt")
            
            #Progrm Commands

            Action = input(f"Enter [add] if you want to add a new account or password.Enter [view] if you want to view your existing accounts or passwords.Enter [exit] if you want to exit").strip().lower()
            
            #ADD Mode:
            if Action.strip() == "add":
                #ADD INPUTS:
                #get inputs
                identifier = get_user_identifier()
                account = get_user_account()
                password = get_user_password()    

                #store data securely 
                key = generate_encryption_key(seed_phrase)
                store_encrypted_data(identifier, account, password, key)

            
            #VIEW Mode
            elif Action.strip() == "view":

                #Retrieve and display accounts
                key = generate_encryption_key(seed_phrase)

                accounts = retrieve_and_decrypt_data(key)

                for identifier, account, password in accounts:
                    print(f"Identifier:{identifier} | Account:{account} | Password:{password}")
                
                else:
                    print("No accounts founds.")






                pass
            
            #EXIT MODE
            elif Action.strip() == "exit":
                running = False
     
        

    #INVALID OUTPUT
        #Error message if invalid output.
    else:
        print("Invalid input! Please enter [y] or [n].")
        return





if __name__ == "__main__":
    main()

