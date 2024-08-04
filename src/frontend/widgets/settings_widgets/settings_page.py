import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.frontend.ui_constants import ui_constants
from src.frontend.widgets.settings_widgets.settings_button import SettingsButton

FONT = ui_constants.FONT
FONTSIZE = ui_constants.FONTSIZE
BACKGROUND_COLOR = ui_constants.BACKGROUND_COLOR
HEADER_COLOR = ui_constants.HEADER_COLOR
ACCENT_COLOR = ui_constants.ACCENT_COLOR
TEXT_COLOR = ui_constants.TEXT_COLOR

class SettingsPage():
    def __init__(self, parent, text):
        self.name = text
        
        self.button = SettingsButton(parent.sidebar_frame, text=self.name, command=lambda: parent.show_page(self.name))

        self.page = tk.Frame(parent.main_frame)
        self.page.config(bg=BACKGROUND_COLOR, padx=5, pady=5)