# main.py

from ui.app import TaskOrganizerApp
from utils.logger import log_error
from tkinter import messagebox
import os

# Diretório base do executável
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HISTORY_FILE = os.path.join(BASE_DIR, "task_history.txt")


def main():
    try:
        app = TaskOrganizerApp(base_dir=BASE_DIR)
        app.mainloop()
    except Exception as e:
        log_error(HISTORY_FILE, f"Unhandled Exception: {e}")
        messagebox.showerror("Unhandled Exception", f"An error occurred: {e}")


if __name__ == "__main__":
    main()
