# ui/notes.py

import tkinter as tk
from tkinter import ttk
from markdown2 import markdown
from utils.logger import log_history


class NotesEditor:
    def __init__(self, parent, task, save_tasks_callback, history_file):
        self.task = task
        self.save_tasks = save_tasks_callback
        self.history_file = history_file

        # Criar janela flutuante
        self.notes_window = tk.Toplevel(parent)
        self.notes_window.title(f"Notes for {task.title}")
        self.notes_window.geometry("600x400")

        # Caixa de texto para edição de anotações
        self.text_editor = tk.Text(self.notes_window)
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text_editor.insert(tk.END, task.notes)

        # Botão para salvar e renderizar Markdown
        render_button = ttk.Button(self.notes_window, text="Save & Render", command=self.save_and_render)
        render_button.pack(pady=5)

        # Visualizador de Markdown
        self.markdown_viewer = tk.Text(self.notes_window, state=tk.DISABLED, wrap=tk.WORD)
        self.markdown_viewer.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.save_and_render()

    def save_and_render(self):
        self.task.notes = self.text_editor.get("1.0", tk.END).strip()
        self.task.update_date_modified()
        self.save_tasks()
        log_history(self.history_file, f"Notes updated for {self.task.title}")

        # Renderizar Markdown
        rendered_markdown = markdown(self.task.notes)
        self.markdown_viewer.config(state=tk.NORMAL)
        self.markdown_viewer.delete("1.0", tk.END)
        self.markdown_viewer.insert(tk.END, rendered_markdown)
        self.markdown_viewer.config(state=tk.DISABLED)
