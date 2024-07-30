import tkinter as tk
from tkinter import ttk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.frontend.ui_constants import *
from src.backend.chat_manager import ChatManager
from src.backend.model_manager import ModelManager
from src.frontend.widgets.chat_widgets.entry_field import EntryField

class ChatWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)

        # Initialize ChatManager
        self.chat_manager = ChatManager()
        self.model_manager = ModelManager()

        # Create a frame for the top menu
        self.top_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.top_frame.pack(fill=tk.X)

        # Configure grid layout for the top frame
        self.top_frame.grid_columnconfigure(0, weight=1, uniform="column")
        self.top_frame.grid_columnconfigure(1, weight=1, uniform="column")
        self.top_frame.grid_columnconfigure(2, weight=1, uniform="column")

        # Define the style for the Combobox
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TCombobox',
                        fieldbackground=BACKGROUND_COLOR,
                        background=BACKGROUND_COLOR,
                        foreground=TEXT_COLOR,
                        font=(FONT, FONTSIZE))
        style.map('TCombobox', 
                  fieldbackground=[('readonly', BACKGROUND_COLOR)],
                  background=[('readonly', BACKGROUND_COLOR)],
                  foreground=[('readonly', TEXT_COLOR)])
        
        # Add a dropdown menu for chat selection
        self.selected_chat = tk.StringVar()
        self.chat_dropdown = ttk.Combobox(self.top_frame, textvariable=self.selected_chat, state='readonly', font=(FONT, FONTSIZE))
        self.chat_dropdown.grid(row=0, column=0, padx=10, sticky='w')
        self.chat_dropdown.bind("<<ComboboxSelected>>", self.change_chat)

        # Add a dropdown menu for model selection
        self.selected_model = tk.StringVar()
        self.model_dropdown = ttk.Combobox(self.top_frame, textvariable=self.selected_model, state='readonly', font=(FONT, FONTSIZE))
        self.model_dropdown.grid(row=0, column=1, padx=10)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.change_model)

        # Add a new chat button
        self.new_chat_button = tk.Button(self.top_frame, text="+", command=self.create_new_chat, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        self.new_chat_button.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        # Create new chat
        self.create_new_chat()

        # Initialize Model List
        self.selected_model.set(self.model_manager.current_model)
        self.refresh_model_list()

        # Create and pack the entry field at the bottom
        self.entry_field = EntryField(self)
        self.entry_field.pack(fill=tk.X, side=tk.BOTTOM, pady=10, padx=10)
    
    def refresh(self):
        self.refresh_chat_list()
        self.refresh_model_list()

    def refresh_chat_list(self):
        self.chat_dropdown['values'] = self.chat_manager.list_chats()

    def change_chat(self, event=None):
        selected_chat = self.selected_chat.get()
        if selected_chat:
            self.chat_manager.change_chat(selected_chat)
            self.refresh_chat_list()

    def create_new_chat(self):
        self.chat_manager.create_new_chat()
        self.selected_chat.set(self.chat_manager.get_current_chat())
        self.change_chat()
    
    def remove_chat(self):
        self.chat_manager.remove_chat()
        self.selected_chat.set(self.chat_manager.get_current_chat())
        self.change_chat()
    
    def refresh_model_list(self):
        self.model_dropdown['values'] = self.model_manager.list_models()

    def change_model(self, event=None):
        selected_model = self.selected_model.get()
        if selected_model:
            self.model_manager.change_model(selected_model)
            self.refresh_model_list()