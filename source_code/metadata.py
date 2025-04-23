import json
import os
from datetime import datetime

# Path to store metadata
METADATA_FILE = "metadata.json"

# Function to load existing metadata
def load_metadata():
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading metadata file: {e}")
            return {}
    else:
        return {}

# Function to save metadata to a file
def save_metadata(metadata):
    try:
        with open(METADATA_FILE, 'w') as file:
            json.dump(metadata, file, indent=4)
    except Exception as e:
        print(f"Error writing to metadata file: {e}")

# Function to add file metadata
def add_file_metadata(file_name: str, encrypted: bool):
    metadata = load_metadata()

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add metadata for the file
    metadata[file_name] = {
        'timestamp': timestamp,
        'encrypted': encrypted
    }

    # Save the updated metadata
    save_metadata(metadata)
    print(f"Metadata for {file_name} added successfully.")

# Function to retrieve metadata
def get_file_metadata(file_name: str):
    metadata = load_metadata()
    if file_name in metadata:
        return metadata[file_name]
    else:
        print(f"No metadata found for {file_name}.")
        return None

# Function to list all files in metadata
def list_all_metadata():
    metadata = load_metadata()
    if metadata:
        metadata_info = "\n".join(
            f"{file_name}: {details}" for file_name, details in metadata.items()
        )
        return metadata_info
    else:
        return "No metadata available."

# Test the metadata system
if __name__ == "__main__":
    action = input("Do you want to (A)dd metadata, (G)et metadata, or (L)ist all metadata? ").lower()

    if action == "a":
        file_name = input("Enter file name: ")
        encrypted = input("Is the file encrypted? (yes/no): ").lower() == "yes"
        add_file_metadata(file_name, encrypted)
    elif action == "g":
        file_name = input("Enter file name to get metadata: ")
        metadata = get_file_metadata(file_name)
        if metadata:
            print(metadata)
    elif action == "l":
        print(list_all_metadata())  # Now returns the metadata info
    else:
        print("Invalid option.")
