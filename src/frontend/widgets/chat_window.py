import tkinter as tk
from tkinter import ttk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.backend.constants import *

class ChatWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)

        # Create a frame for the top menu
        self.top_frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        self.top_frame.pack(fill=tk.X)

        # Add a dropdown menu for chat selection
        self.selected_chat = tk.StringVar()
        self.chat_dropdown = ttk.Combobox(self.top_frame, textvariable=self.selected_chat, state='readonly', font=(FONT, FONTSIZE))
        self.chat_dropdown.pack(side=tk.LEFT, padx=10)
        #self.chat_dropdown.bind("<<ComboboxSelected>>", self.change_chat)

        # Add a dropdown menu for model selection
        self.selected_model = tk.StringVar()
        self.model_dropdown = ttk.Combobox(self.top_frame, textvariable=self.selected_chat, state='readonly', font=(FONT, FONTSIZE))
        self.model_dropdown.pack(side=tk.LEFT, padx=10)
        #self.chat_dropdown.bind("<<ComboboxSelected>>", self.change_model)

        # Add a new chat button
        self.new_chat_button = tk.Button(self.top_frame, text="+", font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        self.new_chat_button.pack(side=tk.RIGHT, padx=5, pady=5)
