# ui/app.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk
from models.task import Task
from utils.tooltip import Tooltip
from utils.logger import log_history
import json
import os


class TaskOrganizerApp(ThemedTk):
    def __init__(self, base_dir):
        super().__init__(theme="breeze")
        self.title("Task Organizer")
        self.geometry("750x600")
        self.configure(bg="#f4f4f4")

        # Diretório base e arquivos de persistência
        self.base_dir = base_dir
        self.task_file = os.path.join(self.base_dir, "tasks.json")
        self.history_file = os.path.join(self.base_dir, "task_history.txt")
        self.tasks = []

        # Carregar tarefas do arquivo
        self.load_tasks()

        # Elementos da Interface Gráfica
        self.task_frame = ttk.Frame(self, padding="10 10 10 10")
        self.task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        task_entry_frame = ttk.Frame(self)
        task_entry_frame.pack(pady=10)

        ttk.Label(task_entry_frame, text="Task Title:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(0, 10))
        self.task_entry = ttk.Entry(task_entry_frame, width=50)
        self.task_entry.pack(side=tk.LEFT)

        self.add_task_button = ttk.Button(self, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.update_task_list()

    def add_task(self):
        task_title = self.task_entry.get()
        if not task_title:
            messagebox.showwarning("Input Error", "Please enter a task title.")
            return
        task = Task(task_title)
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.update_task_list()
        self.save_tasks()
        log_history(self.history_file, f"Task created: {task_title}")

    def toggle_task(self, task):
        task.is_done = not task.is_done
        task.update_date_modified()
        self.update_task_list()
        self.save_tasks()
        log_history(self.history_file, f"Task {'completed' if task.is_done else 'reopened'}: {task.title}")

    def add_subtask(self, parent_task):
        subtask_title = simpledialog.askstring("New Subtask", "Enter subtask title:")
        if not subtask_title:
            return
        subtask = Task(subtask_title)
        parent_task.subtasks.append(subtask)
        parent_task.update_date_modified()
        self.update_task_list()
        self.save_tasks()
        log_history(self.history_file, f"Subtask added to {parent_task.title}: {subtask_title}")

    def delete_task(self, task, parent_task=None):
        if parent_task:
            parent_task.subtasks.remove(task)
            parent_task.update_date_modified()
            log_history(self.history_file, f"Subtask deleted from {parent_task.title}: {task.title}")
        else:
            self.tasks.remove(task)
            log_history(self.history_file, f"Task deleted: {task.title}")
        self.update_task_list()
        self.save_tasks()

    def update_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            task_frame = ttk.Frame(self.task_frame, relief=tk.RAISED, borderwidth=1)
            task_frame.pack(fill=tk.X, padx=5, pady=5)

            task_checkbox_var = tk.BooleanVar(value=task.is_done)
            task_checkbox = ttk.Checkbutton(
                task_frame,
                text=f"{task.title}",
                variable=task_checkbox_var,
                command=lambda t=task: self.toggle_task(t)
            )
            task_checkbox.pack(side=tk.LEFT, padx=10)

            add_subtask_button = ttk.Button(
                task_frame,
                text="Add Subtask",
                command=lambda t=task: self.add_subtask(t)
            )
            add_subtask_button.pack(side=tk.RIGHT, padx=5, pady=5)

            delete_task_button = ttk.Button(
                task_frame,
                text="Delete",
                command=lambda t=task: self.delete_task(t)
            )
            delete_task_button.pack(side=tk.RIGHT, padx=5, pady=5)

            Tooltip.bind(task_checkbox, f"Created: {task.date_created}\nModified: {task.date_modified}")

            if task.subtasks:
                completed_subtasks = sum(1 for subtask in task.subtasks if subtask.is_done)
                progress = int((completed_subtasks / len(task.subtasks)) * 100)
                progress_bar = ttk.Progressbar(task_frame, length=100, value=progress)
                progress_bar.pack(side=tk.RIGHT, padx=10)

                for subtask in task.subtasks:
                    subtask_frame = ttk.Frame(self.task_frame)
                    subtask_frame.pack(fill=tk.X, padx=30, pady=2)

                    subtask_checkbox_var = tk.BooleanVar(value=subtask.is_done)
                    subtask_checkbox = ttk.Checkbutton(
                        subtask_frame,
                        text=f"- {subtask.title}",
                        variable=subtask_checkbox_var,
                        command=lambda st=subtask: self.toggle_task(st)
                    )
                    subtask_checkbox.pack(side=tk.LEFT)

                    delete_subtask_button = ttk.Button(
                        subtask_frame,
                        text="Delete",
                        command=lambda st=subtask, pt=task: self.delete_task(st, pt)
                    )
                    delete_subtask_button.pack(side=tk.RIGHT, padx=5, pady=2)

                    Tooltip.bind(subtask_checkbox, f"Created: {subtask.date_created}\nModified: {subtask.date_modified}")

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
