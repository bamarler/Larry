import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.frontend.ui_constants import *

class UserPrompt(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(bg=ACCENT_COLOR)

        self.text_widget = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, font=(FONT, FONTSIZE), bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0)
        self.text_widget.pack(side=tk.TOP, padx=10, pady=10, fill=tk.NONE)

        self.bind('<KeyRelease>', self._resize)

    def get_text(self):
        return self.text_widget.text_widget.get("1.0", "end-1c")

    def set_text(self, text):
        self.text_widget.config(state=tk.NORMAL)  # Make the text widget editable
        self.text_widget.delete('1.0', tk.END)  # Clear existing text
        self.text_widget.insert(tk.END, text)  # Insert new text
        self.text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
        self._resize()

    def _resize(self, event=None):
        # Calculate the number of lines and columns in the text widget
        lines = int(self.text_widget.index('end-1c').split('.')[0])
        max_length = max(len(line) for line in self.text_widget.get('1.0', 'end-1c').split('\n'))

        #parent_width = self.master.winfo_width()

        #if max_length > parent_width:
        #    max_length = parent_width

        # Set the height and width of the text widget
        self.text_widget.config(height=lines, width=max_length)