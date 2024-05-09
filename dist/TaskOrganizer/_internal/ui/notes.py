# ui/notes.py

import tkinter as tk
from tkinter import ttk
from utils.logger import log_history
import webbrowser
import os
import tempfile
from mistletoe import markdown


class NotesEditor:
    def __init__(self, parent, task, save_tasks_callback, history_file):
        self.task = task
        self.save_tasks = save_tasks_callback
        self.history_file = history_file

        # Criar janela flutuante
        self.notes_window = tk.Toplevel(parent)
        self.notes_window.title(f"Notes for {task.title}")
        self.notes_window.geometry("800x600")

        # Frame principal
        main_frame = ttk.Frame(self.notes_window, padding=(10, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Caixa de texto para edição de anotações
        self.text_editor = tk.Text(main_frame, height=10)
        self.text_editor.grid(row=0, column=0, sticky="nsew")
        self.text_editor.insert(tk.END, task.notes)

        # Botão para salvar e renderizar Markdown no navegador
        render_button = ttk.Button(main_frame, text="Save & View", command=self.save_and_view)
        render_button.grid(row=1, column=0, pady=5, sticky="ew")

        # Ajuste das proporções dos elementos
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def save_and_view(self):
        # Salvar anotação como Markdown
        self.task.notes = self.text_editor.get("1.0", tk.END).strip()
        self.task.update_date_modified()
        self.save_tasks()
        log_history(self.history_file, f"Notes updated for {self.task.title}")

        # Converter para HTML usando mistletoe
        rendered_markdown = markdown(self.task.notes)

        # Estilos CSS para renderização
        styles = """
        <style>
            body {
                font-family: "Open Sans", Arial, sans-serif;
                line-height: 1.6;
                color: #1c1c1c;
                padding: 10px;
                margin: 0;
                background-color: #f8f9fa;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #2c3e50;
                font-weight: bold;
            }
            pre {
                background-color: #f4f4f4;
                border-left: 3px solid #ccc;
                padding: 10px;
                overflow-x: auto;
                font-family: Consolas, 'Courier New', monospace;
            }
            code {
                background-color: #f4f4f4;
                border-radius: 3px;
                padding: 2px 4px;
                font-size: 0.9em;
                font-family: Consolas, 'Courier New', monospace;
            }
            ul, ol {
                margin-left: 20px;
            }
            blockquote {
                margin: 0;
                padding-left: 10px;
                border-left: 3px solid #ccc;
                color: #555;
            }
            a {
                color: #3498db;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
        """

        # HTML final com estilos embutidos
        html_content = f"<html><head>{styles}</head><body>{rendered_markdown}</body></html>"

        # Salvar HTML em um arquivo temporário
        temp_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        with open(temp_html_file.name, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Abrir o arquivo HTML no navegador padrão
        webbrowser.open(f"file://{os.path.abspath(temp_html_file.name)}")
