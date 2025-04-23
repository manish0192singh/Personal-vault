import logging

# Set up logging configuration
def setup_logging():
    logging.basicConfig(
        filename='vault_log.log',  # Log file path
        level=logging.INFO,  # Log level
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
        datefmt='%Y-%m-%d %H:%M:%S',  # Date format
        force=True  # Force reset existing logging configuration
    )

# Function to log an event
def log_event(message: str, level: str = 'INFO'):
    if level.upper() == 'INFO':
        logging.info(message)
    elif level.upper() == 'WARNING':
        logging.warning(message)
    elif level.upper() == 'ERROR':
        logging.error(message)
    elif level.upper() == 'DEBUG':
        logging.debug(message)
    else:
        logging.info(message)

# Test the logging system
if __name__ == "__main__":
    setup_logging()
    log_event("Vault system initialized.")
    log_event("User attempted to log in.", 'INFO')
    log_event("User failed login attempt.", 'WARNING')
    log_event("File uploaded successfully.", 'INFO')
    log_event("System error occurred.", 'ERROR')
