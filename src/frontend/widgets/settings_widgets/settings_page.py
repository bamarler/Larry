import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.frontend.ui_constants import *
from src.frontend.widgets.settings_widgets.settings_button import SettingsButton

class SettingsPage():
    def __init__(self, parent, text):
        self.name = text
        
        self.button = SettingsButton(parent.sidebar_frame, text=self.name, command=lambda: parent.show_page(self.name))

        self.page = tk.Frame(parent.main_frame)
        self.page.config(bg=BACKGROUND_COLOR)