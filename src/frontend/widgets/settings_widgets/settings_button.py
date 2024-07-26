import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))))

from src.frontend.ui_constants import *

class SettingsButton(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent, text=text, command=command, bg=HEADER_COLOR, fg=TEXT_COLOR, bd=0, font=(FONT, FONTSIZE))
        self.pack_propagate(False)