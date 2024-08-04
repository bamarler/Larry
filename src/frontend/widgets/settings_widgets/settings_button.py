import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))))

from src.frontend.ui_constants import ui_constants

FONT = ui_constants.FONT
FONTSIZE = ui_constants.FONTSIZE
BACKGROUND_COLOR = ui_constants.BACKGROUND_COLOR
HEADER_COLOR = ui_constants.HEADER_COLOR
ACCENT_COLOR = ui_constants.ACCENT_COLOR
TEXT_COLOR = ui_constants.TEXT_COLOR

class SettingsButton(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent, text=text, command=command, bg=HEADER_COLOR, fg=TEXT_COLOR, bd=0, font=(FONT, FONTSIZE))
        self.pack_propagate(False)