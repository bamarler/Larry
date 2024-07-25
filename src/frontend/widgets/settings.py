import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.backend.constants import *

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

        # Initialize list to keep track of buttons and pages
        self.buttons = []
        self.pages = []
        self.current_page = None
        self.current_button = None

        self.init_buttons()  # Initialize the buttons and pages
        self.show_page(0)

    def init_buttons(self):
        self.init_testPage1()
        self.init_testPage2()

        for button in self.buttons:
            button.pack(fill=tk.BOTH, padx=10, pady=5)
    
    def init_testPage1(self):
        testButton1 = SettingsButton(self.sidebar_frame, text="test button 1", command=lambda: self.show_page(0))
        self.buttons.append(testButton1)

        testPage1 = SettingsPage(self.main_frame)
        testPage1.config(bg=BACKGROUND_COLOR)
        self.pages.append(testPage1)
    
    def init_testPage2(self):
        testButton2 = SettingsButton(self.sidebar_frame, text="test button 2", command=lambda: self.show_page(1))
        self.buttons.append(testButton2)

        testPage2 = SettingsPage(self.main_frame)
        testPage2.config(bg=BACKGROUND_COLOR)
        self.pages.append(testPage2)

    def show_page(self, index):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = self.pages[index]
        self.current_page.pack(fill=tk.BOTH, expand=True)

        # Highlight the current button
        if self.current_button:
            self.current_button.config(bg=HEADER_COLOR)
        self.current_button = self.buttons[index]
        self.current_button.config(bg=BACKGROUND_COLOR)

class SettingsButton(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent, text=text, command=command, bg=HEADER_COLOR, fg=TEXT_COLOR, bd=0, font=(FONT, FONTSIZE))
        self.pack_propagate(False)

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.pack_propagate(False)