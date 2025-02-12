#LIBRARY CALLS:

import hashlib
import random
import base64
from cryptography.fernet import Fernet


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
    with open("hashed_seed.txt", "w") as file:
        file.write(hashed_seed)
    print(f"Stored hashed seed: {hashed_seed}")  # For debugging


# Function to check if the entered seed matches the stored hash
def check_seed_phrase(entered_seed):
    hashed_entered_seed = hash_the_seed_phrase(entered_seed)
    with open("hashed_seed.txt", "r") as file:
        stored_hash = file.read().strip()
    print(f"Entered hash: {hashed_entered_seed}")  # For debugging
    print(f"Stored hash: {stored_hash}")  # For debugging
    return hashed_entered_seed == stored_hash
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
    password = input(f"Enter your password:")
    return password

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

def store_encrypted_data():
    
    pass
    
  


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
            print("Authentication failed. Invalid seed phrase.")

        #ONCE AUTHENTICATED.
        running = True

        while running:
            #Progrm Commands
            Action = input(f"If you want to add a new account and password enter: add.If you want to view your existing accouns or password enter: view.If you want to exit enter: exit")
            #ADD Mode:
            if Action.strip() == "add":
                #ADD INPUTS:

                identifier = get_user_identifier()
                account = get_user_account()
                passowrd = get_user_password()               

                pass
            #VIEW Mode
            elif Action.strip() == "view":
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

