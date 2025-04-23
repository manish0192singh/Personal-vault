import os
from encryption import encrypt_file, decrypt_file

FILE_STORAGE_DIR = "vault_files"

if not os.path.exists(FILE_STORAGE_DIR):
    os.makedirs(FILE_STORAGE_DIR)

def upload_file(filepath):
    try:
        encrypted_path, key_path = encrypt_file(filepath, FILE_STORAGE_DIR)
        return encrypted_path, key_path
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None, None

def retrieve_file(key_file_path):
    try:
        decrypted_path = decrypt_file(key_file_path, FILE_STORAGE_DIR)
        return decrypted_path
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")
