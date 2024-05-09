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

        # Frame principal
        main_frame = ttk.Frame(self.notes_window, padding=(10, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Caixa de texto para edição de anotações
        self.text_editor = tk.Text(main_frame, height=10)
        self.text_editor.grid(row=0, column=0, sticky="nsew")
        self.text_editor.insert(tk.END, task.notes)

        # Botão para salvar e renderizar Markdown
        render_button = ttk.Button(main_frame, text="Save & Render", command=self.save_and_render)
        render_button.grid(row=1, column=0, pady=5, sticky="ew")

        # Visualizador de Markdown
        self.markdown_viewer = tk.Text(main_frame, state=tk.DISABLED, wrap=tk.WORD)
        self.markdown_viewer.grid(row=2, column=0, sticky="nsew")

        # Ajuste das proporções dos elementos
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)

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
