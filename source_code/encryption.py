from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os

# Generate public and private keys if they don't already exist
def generate_keys():
    private_key_file = "private_key.pem"
    public_key_file = "public_key.pem"

    # Only generate if keys don't already exist
    if not os.path.exists(private_key_file) or not os.path.exists(public_key_file):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Save private key
        with open(private_key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Save public key
        with open(public_key_file, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

# Call key generation when script is run
generate_keys()

# Encrypt a file using the public key
def encrypt_file(filepath, vault_dir="vault_files"):
    # Load the public key
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Read the file to encrypt
    with open(filepath, "rb") as f:
        file_data = f.read()

    # Encrypt the file using RSA and OAEP padding
    encrypted_data = public_key.encrypt(
        file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Create output file paths
    enc_file_path = os.path.join(vault_dir, os.path.basename(filepath) + ".enc")
    key_file_path = os.path.join(vault_dir, os.path.basename(filepath) + ".key")

    # Save the encrypted file
    with open(enc_file_path, "wb") as f:
        f.write(encrypted_data)

    # Here we're writing the same encrypted data again just to mimic saving a key
    # In real-world RSA usage, you'd encrypt a symmetric key and save that instead
    with open(key_file_path, "wb") as f:
        f.write(encrypted_data)

    return enc_file_path, key_file_path

# Decrypt a file using the private key (assumes .key file has encrypted data)
def decrypt_file(key_file_path, vault_dir="vault_files"):
    # Load the private key
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Read the encrypted file
    with open(key_file_path, "rb") as f:
        encrypted_data = f.read()

    # Decrypt the data
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Prepare output filename
    original_name = os.path.basename(key_file_path).replace(".key", "")
    output_file = os.path.join(vault_dir, "decrypted_" + original_name)

    # Save decrypted data
    with open(output_file, "wb") as f:
        f.write(decrypted_data)

    return output_file

# Used to decrypt a file encrypted by someone else using our public key
def decrypt_external_file(enc_file, key_file, private_key_file):
    # Load private key
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Read the encrypted key file (contains actual data in this example)
    with open(key_file, "rb") as f:
        encrypted_data = f.read()

    # Decrypt the data
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Save the output as a new file
    output_file = enc_file.replace(".enc", "_decrypted")
    with open(output_file, "wb") as f:
        f.write(decrypted_data)

    return output_file
