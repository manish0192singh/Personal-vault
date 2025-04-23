import bcrypt
import json
import os

# This file will store all registered users and their hashed passwords
USER_CREDENTIALS_FILE = "user_credentials.json"

# Hash the password so it's not saved in plain text
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Check if the entered password matches the stored hashed password
def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

# Register a new user and store their username and hashed password
def register_user(username, password):
    try:
        # Check if credentials file exists, otherwise start with an empty dict
        if os.path.exists(USER_CREDENTIALS_FILE):
            with open(USER_CREDENTIALS_FILE, 'r') as file:
                users = json.load(file)
        else:
            users = {}

        # Prevent duplicate usernames
        if username in users:
            print("Username already taken!")
            return False

        # Save the new user with their hashed password
        users[username] = hash_password(password)

        # Write updated users back to the file
        with open(USER_CREDENTIALS_FILE, 'w') as file:
            json.dump(users, file)

        print("User registered successfully.")
        return True

    except Exception as e:
        print("Something went wrong during registration:", e)
        return False

# Login a user by checking their password
def login_user(username, password):
    try:
        # Load user data
        if os.path.exists(USER_CREDENTIALS_FILE):
            with open(USER_CREDENTIALS_FILE, 'r') as file:
                users = json.load(file)
        else:
            print("No users found.")
            return False

        # Check username and verify password
        if username in users and verify_password(users[username], password):
            print("Login successful!")
            return True
        else:
            print("Wrong username or password.")
            return False

    except Exception as e:
        print("Something went wrong during login:", e)
        return False

# Test registration and login from command line
if __name__ == "__main__":
    choice = input("Do you want to (R)egister or (L)ogin? ").lower()

    if choice == "r":
        uname = input("Choose a username: ")
        pwd = input("Choose a password: ")
        register_user(uname, pwd)

    elif choice == "l":
        uname = input("Enter your username: ")
        pwd = input("Enter your password: ")
        login_user(uname, pwd)

    else:
        print("Invalid option selected.")
