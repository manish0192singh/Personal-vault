import smtplib
from email.mime.text import MIMEText
import json
import os

# Load email credentials from config file
def load_email_config():
    try:
        # Path to the config file
        config_file = 'config/email_config.json'

        # Check if file exists
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"{config_file} not found.")

        # Open and read the JSON config
        with open(config_file, 'r') as file:
            return json.load(file)
    except Exception as e:
        print("Could not load email config:", e)
        raise

# Function to send an alert email
def send_email_alert(subject, body):
    try:
        # Get email details from config file
        config = load_email_config()
        sender_email = config['sender_email']
        sender_password = config['sender_password']
        receiver_email = config['receiver_email']

        # Create the email message (plain text)
        msg = MIMEText(body)
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Use Gmail's SMTP server (SSL on port 465)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email alert sent.")
    except Exception as e:
        print("Error sending email alert:", e)

# Just for testing purpose – will only run if this file is run directly
if __name__ == "__main__":
    test_subject = "Unauthorized Access"
    test_body = "Someone tried to access the vault without permission."
    send_email_alert(test_subject, test_body)
