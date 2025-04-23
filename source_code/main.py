import tkinter as tk
from tkinter import messagebox, filedialog
from authentication import register_user, login_user
from encryption import encrypt_file, decrypt_file, decrypt_external_file
from file_oprations import upload_file, retrieve_file, delete_file
from logging_system import setup_logging, log_event
from metadata import add_file_metadata, get_file_metadata, list_all_metadata
from alerting import send_email_alert
import os
import json

class PersonalVaultApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Personal Vault")
        self.root.geometry("400x500")
        self.username = None

        # Show login screen first
        self.show_login_screen()

    def show_login_screen(self):
        # Clear existing widgets in case they exist
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title Label
        title_label = tk.Label(self.root, text="Personal Vault", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(fill=tk.X, pady=10)

        # Username Entry
        tk.Label(self.root, text="Username:", font=("Arial", 12), bg="#e8f5e9").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="solid", width=25)
        self.username_entry.pack(pady=5)

        # Password Entry
        tk.Label(self.root, text="Password:", font=("Arial", 12), bg="#e8f5e9").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), bd=2, relief="solid", width=25)
        self.password_entry.pack(pady=5)

        # Gmail Entry for registration
        tk.Label(self.root, text="Gmail (for alerts - only needed for registration):", font=("Arial", 12), bg="#e8f5e9").pack(pady=5)
        self.gmail_entry = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="solid", width=25)
        self.gmail_entry.pack(pady=5)

        # Buttons
        login_button = tk.Button(self.root, text="Login", command=self.login, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", bd=2)
        login_button.pack(pady=10)

        register_button = tk.Button(self.root, text="Register", command=self.register, font=("Arial", 12), bg="#FF5722", fg="white", relief="solid", bd=2)
        register_button.pack(pady=10)

        self.root.configure(bg="#e8f5e9")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate user login
        if login_user(username, password):
            log_event(f"{username} logged in successfully.")
            self.username = username
            self.show_main_menu()
        else:
            log_event(f"Failed login attempt for {username}.", "WARNING")
            send_email_alert("Unauthorized Access Attempt", f"Failed login for user: {username}")
            messagebox.showerror("Error", "Invalid credentials!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_email = self.gmail_entry.get()

        # Ensure a valid Gmail address is entered
        if not user_email or "@gmail.com" not in user_email:
            messagebox.showerror("Error", "Please enter a valid Gmail address for registration.")
            return

        # Save receiver email in config
        config_path = "config/email_config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config_data = json.load(f)
        else:
            config_data = {}

        config_data["receiver_email"] = user_email

        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)

        # Register user
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered and email saved!")
        else:
            messagebox.showerror("Error", "User already exists!")

    def show_main_menu(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#e8f5e9")

        # Main Menu Title
        title_label = tk.Label(self.root, text="Welcome to Personal Vault", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(pady=20, ipadx=10, ipady=5)

        # Menu Buttons
        button_style = {
            "font": ("Arial", 12),
            "width": 20,
            "relief": "solid",
            "bd": 2,
            "padx": 10,
            "pady": 6
        }

        # Action Buttons
        tk.Button(self.root, text="Upload File", command=self.upload_file, bg="#4CAF50", fg="white", **button_style).pack(pady=5)
        tk.Button(self.root, text="Retrieve File", command=self.retrieve_file, bg="#4CAF50", fg="white", **button_style).pack(pady=5)
        tk.Button(self.root, text="Delete File", command=self.delete_file, bg="#FF5722", fg="white", **button_style).pack(pady=5)
        tk.Button(self.root, text="Decrypt Shared File", command=self.decrypt_shared_file, bg="#2196F3", fg="white", **button_style).pack(pady=5)
        tk.Button(self.root, text="View Logs", command=self.view_logs, bg="#FF5722", fg="white", **button_style).pack(pady=5)
        tk.Button(self.root, text="View Metadata", command=self.view_metadata, bg="#FF5722", fg="white", **button_style).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.show_login_screen, bg="#FFC107", fg="white", **button_style).pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            enc_path, key_path = upload_file(file_path)
            if enc_path and key_path:
                add_file_metadata(file_path, True)
                log_event(f"File uploaded: {file_path}")
                messagebox.showinfo("Success", f"File encrypted: {os.path.basename(enc_path)}\nKey File: {os.path.basename(key_path)}")
            else:
                messagebox.showerror("Error", "File upload failed. See logs.")

    def retrieve_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            output = retrieve_file(file_path)
            if output:
                log_event(f"File retrieved: {file_path}")
                messagebox.showinfo("Success", "File retrieved and decrypted successfully!")
            else:
                messagebox.showerror("Error", "File decryption failed.")

    def delete_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            delete_file(file_path)
            log_event(f"File deleted: {file_path}")
            messagebox.showinfo("Success", "File deleted successfully!")

    def decrypt_shared_file(self):
        enc_file = filedialog.askopenfilename(title="Select .enc File")
        key_file = filedialog.askopenfilename(title="Select .key.enc File")
        private_key_file = filedialog.askopenfilename(title="Select Your Private Key (.pem)")

        if enc_file and key_file and private_key_file:
            try:
                output_file = decrypt_external_file(enc_file, key_file, private_key_file)
                messagebox.showinfo("Success", f"Decrypted as: {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt shared file: {str(e)}")

    def view_logs(self):
        try:
            with open("vault_log.log", "r") as log_file:
                all_logs = log_file.readlines()
                recent_logs = all_logs[-5:]
                log_text = "".join(recent_logs)
        except FileNotFoundError:
            log_text = "No logs available."

        messagebox.showinfo("Recent Logs", log_text)

    def view_metadata(self):
        metadata_info = list_all_metadata()
        messagebox.showinfo("Metadata", metadata_info)

# Run the application
if __name__ == "__main__":
    setup_logging()  # Initialize logging
    root = tk.Tk()
    app = PersonalVaultApp(root)
    root.mainloop()
