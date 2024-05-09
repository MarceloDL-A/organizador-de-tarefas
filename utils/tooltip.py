# utils/tooltip.py

import tkinter as tk


class Tooltip:
    @staticmethod
    def bind(widget, text):
        tooltip = tk.Toplevel(widget, bg="white", padx=5, pady=5)
        tooltip.overrideredirect(True)
        tooltip.withdraw()
        tooltip_label = tk.Label(tooltip, text=text, justify=tk.LEFT, bg="white", relief=tk.SOLID, borderwidth=1, font=("Arial", 10))
        tooltip_label.pack()

        def enter(event):
            tooltip.deiconify()
            tooltip.lift()
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
