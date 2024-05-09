# ui/app.py

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from models.task import Task
from utils.logger import log_history
from ui.task_list import TaskList
import json
import os


class TaskOrganizerApp(ThemedTk):
    def __init__(self, base_dir):
        super().__init__(theme="breeze")
        self.title("Task Organizer")
        self.state("zoomed")  # Abrir em modo maximizado
        self.configure(bg="#f4f4f4")

        # Diretório base e arquivos de persistência
        self.base_dir = base_dir
        self.task_file = os.path.join(self.base_dir, "tasks.json")
        self.history_file = os.path.join(self.base_dir, "task_history.txt")
        self.tasks = []

        # Carregar tarefas do arquivo
        self.load_tasks()

        # Notebook para as abas de "Em Aberto" e "Concluídas"
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Criar as abas
        self.frame_open_tasks = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.frame_completed_tasks = ttk.Frame(self.notebook, padding="10 10 10 10")

        self.notebook.add(self.frame_open_tasks, text="Em Aberto")
        self.notebook.add(self.frame_completed_tasks, text="Concluídas")

        # Gerenciar a lista de tarefas
        self.task_list_open = TaskList(self.frame_open_tasks, self.tasks, self.history_file, self.save_tasks, completed=False, update_callback=self.update_task_lists)
        self.task_list_completed = TaskList(self.frame_completed_tasks, self.tasks, self.history_file, self.save_tasks, completed=True, update_callback=self.update_task_lists)

        # Interface de entrada para novas tarefas
        task_entry_frame = ttk.Frame(self)
        task_entry_frame.pack(pady=10)

        ttk.Label(task_entry_frame, text="Task Title:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(0, 10))
        self.task_entry = ttk.Entry(task_entry_frame, width=50)
        self.task_entry.pack(side=tk.LEFT)

        self.add_task_button = ttk.Button(self, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.update_task_lists()

    def add_task(self):
        task_title = self.task_entry.get()
        if not task_title:
            messagebox.showwarning("Input Error", "Please enter a task title.")
            return
        task = Task(task_title)
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.update_task_lists()
        self.save_tasks()
        log_history(self.history_file, f"Task created: {task_title}")

    def update_task_lists(self):
        self.task_list_open.update_task_list()
        self.task_list_completed.update_task_list()

    def save_tasks(self):
        try:
            with open(self.task_file, "w") as file:
                json.dump([task.to_dict() for task in self.tasks], file, indent=4)
        except Exception as e:
            log_history(self.history_file, f"Error saving tasks: {e}")
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def load_tasks(self):
        print(f"Loading tasks from: {self.task_file}")
        try:
            if os.path.exists(self.task_file):
                with open(self.task_file, "r") as file:
                    tasks_data = json.load(file)
                    self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
            else:
                self.tasks = []
                self.save_tasks()
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", "Failed to load tasks: The task file is corrupted or empty.")
            log_history(self.history_file, f"Error loading tasks: {e}")
            self.tasks = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {e}")
            log_history(self.history_file, f"Error loading tasks: {e}")
            self.tasks = []

def main():
    app = TaskOrganizerApp(base_dir=os.path.dirname(__file__))
    app.mainloop()


if __name__ == "__main__":
    main()
