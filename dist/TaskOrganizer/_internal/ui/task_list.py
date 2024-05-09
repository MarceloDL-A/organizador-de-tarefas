# ui/task_list.py

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from models.task import Task
from ui.notes import NotesEditor
from utils.tooltip import Tooltip
from utils.logger import log_history


class TaskList:
    def __init__(self, parent, tasks, history_file, save_tasks_callback, completed=False, update_callback=None):
        self.parent = parent
        self.tasks = tasks
        self.history_file = history_file
        self.save_tasks = save_tasks_callback
        self.completed = completed
        self.update_callback = update_callback

        # Frame que contém todas as tarefas
        self.task_frame = ttk.Frame(self.parent, padding="10 10 10 10")
        self.task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.update_task_list()

    def update_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            if self._should_display_task(task):
                self._create_task_frame(self.task_frame, task)

    def _should_display_task(self, task):
        if self.completed:
            return task.is_done and self._are_all_subtasks_done(task)
        return not task.is_done or not self._are_all_subtasks_done(task)

    def _are_all_subtasks_done(self, task):
        return all(self._are_all_subtasks_done(subtask) for subtask in task.subtasks) if task.subtasks else task.is_done

    def _create_task_frame(self, parent_frame, task, parent_task=None, indent=0):
        task_frame = ttk.Frame(parent_frame, relief=tk.RAISED, borderwidth=1)
        task_frame.pack(fill=tk.X, padx=(indent, 5), pady=5)

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

        notes_button = ttk.Button(
            task_frame,
            text="Notes",
            command=lambda t=task: NotesEditor(self.parent, t, self.save_tasks, self.history_file)
        )
        notes_button.pack(side=tk.RIGHT, padx=5, pady=5)

        delete_task_button = ttk.Button(
            task_frame,
            text="Delete",
            command=lambda t=task, pt=parent_task: self.delete_task(t, pt)
        )
        delete_task_button.pack(side=tk.RIGHT, padx=5, pady=5)

        Tooltip.bind(task_checkbox, f"Created: {task.date_created}\nModified: {task.date_modified}")

        if task.subtasks:
            completed_subtasks = sum(1 for subtask in task.subtasks if subtask.is_done)
            progress = int((completed_subtasks / len(task.subtasks)) * 100)
            progress_bar = ttk.Progressbar(task_frame, length=100, value=progress)
            progress_bar.pack(side=tk.RIGHT, padx=10)

            for subtask in task.subtasks:
                self._create_task_frame(parent_frame, subtask, parent_task=task, indent=indent + 20)

    def toggle_task(self, task):
        task.is_done = not task.is_done
        task.update_date_modified()
        self.save_tasks()
        log_history(self.history_file, f"Task {'completed' if task.is_done else 'reopened'}: {task.title}")

        if self.update_callback:
            self.update_callback()

    def add_subtask(self, parent_task):
        subtask_title = simpledialog.askstring("New Subtask", "Enter subtask title:")
        if not subtask_title:
            return
        subtask = Task(subtask_title)
        parent_task.subtasks.append(subtask)
        parent_task.update_date_modified()
        self.save_tasks()
        log_history(self.history_file, f"Subtask added to {parent_task.title}: {subtask_title}")

        if self.update_callback:
            self.update_callback()

    def delete_task(self, task, parent_task=None):
        confirm = messagebox.askyesno("Delete Task", f"Are you sure you want to delete '{task.title}'?")
        if not confirm:
            return

        if parent_task:
            parent_task.subtasks.remove(task)
            parent_task.update_date_modified()
            log_history(self.history_file, f"Subtask deleted from {parent_task.title}: {task.title}")
        else:
            self.tasks.remove(task)
            log_history(self.history_file, f"Task deleted: {task.title}")

        self.save_tasks()

        if self.update_callback:
            self.update_callback()
