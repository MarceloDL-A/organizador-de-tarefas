# utils/logger.py

from datetime import datetime


def log_history(file, message):
    with open(file, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


def log_error(file, message):
    log_history(file, f"Error: {message}")
