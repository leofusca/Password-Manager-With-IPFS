import hashlib
import random

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


def main():
    # Load the word list from the file (replace 'wordlist' with your actual wordlist file name)
    word_list = load_word_list("wordlist")
    
    # Ask user if they already have a seed phrase
    user_input = input("Do you have a seed phrase already? Press [y] if you have, [n] if you don't: ").strip().lower()

    if user_input == "n":

        # If no seed, generate one
        seed_phrase = generate_seed_phrase(word_list)
        # Store the generated seed in a secure place (for demo, we're storing the hashed version)
        hashed_seed = hash_the_seed_phrase(seed_phrase)
        store_hashed_seed(hashed_seed)
        print(f"Generated seed phrase: {seed_phrase}")
        print("Seed phrase stored securely!")



    elif user_input == "y":

        # If user already has a seed phrase, let them input it
        seed_phrase = get_user_seed_phrase()
        hashed_seed = hash_the_seed_phrase(seed_phrase)
        # 3. Login functionality (for the user to check if the seed matches)
                
        if check_seed_phrase(seed_phrase):
            print("Authentication successful!")
        else:
            print("Authentication failed. Invalid seed phrase.")


    else:
        print("Invalid input! Please enter [y] or [n].")
        return




if __name__ == "__main__":
    main()

