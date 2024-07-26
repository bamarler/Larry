import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.frontend.ui_constants import *
from src.frontend.widgets.settings_widgets.model_settings import ModelSettingsPage
from src.frontend.widgets.settings_widgets.download_settings_page import DownloadSettingsPage
from src.frontend.widgets.settings_widgets.system_text_settings import SystemTextSettingsPage
from src.frontend.widgets.settings_widgets.theme_settings import ThemeSettingsPage

class Settings(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack_propagate(False)  # Prevent the frame from resizing to its content
        
        self.sidebar_width = parent.winfo_screenwidth() // 12
        self.sidebar_frame = tk.Frame(self, width=self.sidebar_width, bg=HEADER_COLOR)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        self.main_frame = tk.Frame(self, bg=ACCENT_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        self.settings_label = tk.Label(self.sidebar_frame, text="Settings", bg=HEADER_COLOR, fg=TEXT_COLOR, font=(FONT, FONTSIZE))
        self.settings_label.pack(fill=tk.BOTH, padx=10, pady=5)

        # Initialize Pages
        self.model_settings = ModelSettingsPage(self)
        self.download_settings = DownloadSettingsPage(self)
        self.system_text_settings = SystemTextSettingsPage(self)
        self.theme_settings = ThemeSettingsPage(self)

        # Initialize list to keep track of buttons and pages
        self.pages = []
        self.current_page = None
        self.current_button = None

        self.init_pages()  # Initialize the buttons
        self.show_page(self.pages[0].name)

    def init_pages(self):
        self.pages.append(self.model_settings)
        self.pages.append(self.download_settings)
        self.pages.append(self.system_text_settings)
        self.pages.append(self.theme_settings)

        for page in self.pages:
            page.button.pack(fill=tk.BOTH, padx=10, pady=5)

    def show_page(self, name):
        if self.current_page:
            self.current_page.pack_forget()
        if self.current_button:
            self.current_button.config(bg=HEADER_COLOR)

        for setting_page in self.pages:
            if setting_page.name == name:
                self.current_page = setting_page.page
                self.current_button = setting_page.button
                self.current_button.config(bg=ACCENT_COLOR)
        
        self.current_page.pack(fill=tk.BOTH, expand=True)
        