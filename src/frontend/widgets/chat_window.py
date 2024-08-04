import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.frontend.ui_constants import ui_constants
from src.backend.chat_manager import ChatManager
from src.backend.model_manager import ModelManager
from src.frontend.widgets.chat_widgets.entry_field import EntryField
from src.frontend.widgets.chat_widgets.user_prompt import UserPrompt
from src.frontend.widgets.chat_widgets.assistant_response import AssistantResponse

FONT = ui_constants.FONT
FONTSIZE = ui_constants.FONTSIZE
BACKGROUND_COLOR = ui_constants.BACKGROUND_COLOR
HEADER_COLOR = ui_constants.HEADER_COLOR
ACCENT_COLOR = ui_constants.ACCENT_COLOR
TEXT_COLOR = ui_constants.TEXT_COLOR

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

        # Initialize last_message_count
        self.last_message_count = 0

        # Initialize Model List
        self.selected_model.set(self.model_manager.current_model)

        # Create and pack the entry field at the bottom
        self.entry_field = EntryField(self, self.send_message)
        self.entry_field.pack(fill=tk.X, side=tk.BOTTOM, pady=10, padx=10)

        # Manage Chat Feed
        self.chat_display_frame = tk.Frame(self, bg=BACKGROUND_COLOR)  # Frame to hold chat widgets
        self.chat_display_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_display_frame, troughcolor=BACKGROUND_COLOR, bg=ACCENT_COLOR)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_canvas = tk.Canvas(self.chat_display_frame, bg=BACKGROUND_COLOR, yscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.chat_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.chat_canvas.yview)

        # Bind mouse wheel to scroll
        self.chat_canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.chat_canvas.bind("<Leave>", self._unbind_from_mousewheel)

        self.chat_frame = tk.Frame(self.chat_canvas, bg=BACKGROUND_COLOR)
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor='nw')

        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        
        self.refresh()

        # Create new chat
        self.create_new_chat()

    def _bind_to_mousewheel(self, event):
        self.chat_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbind_from_mousewheel(self, event):
        self.chat_canvas.unbind_all("<MouseWheel>")

    def refresh(self):
        self.refresh_chat_list()
        self.refresh_model_list()

    def refresh_chat_list(self):
        chats = self.chat_manager.list_chats()

        if self.chat_manager.current_chat_name in chats:
            chats.remove(self.chat_manager.current_chat_name)

        self.chat_dropdown['values'] = chats

    def change_chat(self, event=None):
        selected_chat = self.selected_chat.get()
        if selected_chat:
            self.chat_manager.change_chat(selected_chat)
            self.scroll_to_top()
            self.refresh()
            self.load_chat()
            self.scroll_to_bottom()

    def create_new_chat(self):
        new_chat_name = self.chat_manager.create_new_chat()
        if self.selected_chat.get() == new_chat_name:
            return
        self.selected_chat.set(new_chat_name)
        self.change_chat()
    
    def remove_chat(self):
        self.chat_manager.remove_chat()
        self.selected_chat.set(self.chat_manager.get_current_chat())
        self.change_chat()
    
    def refresh_model_list(self):
        model_names = self.model_manager.list_models()
        self.model_dropdown['values'] = [model for model in model_names if model != self.model_manager.current_model]

    def change_model(self, event=None):
        selected_model = self.selected_model.get()
        if selected_model:
            self.model_manager.change_model(selected_model)
            self.refresh_model_list()
    
    def _on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.chat_canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:
            self.chat_canvas.yview_scroll(-1, "units")
    
    def scroll_to_bottom(self):
        self.chat_canvas.update_idletasks()  # Ensure all pending updates are applied
        self.chat_canvas.yview_moveto(1.0)  # Scroll to the bottom

    def scroll_to_top(self):
        self.chat_canvas.update_idletasks()  # Ensure all pending updates are applied
        self.chat_canvas.yview_moveto(0.0)  # Scroll to the top

    def load_chat(self):
        # Clear the canvas of any widgets
        for widget in self.chat_frame.winfo_children():
            widget.pack_forget()
            widget.destroy()
        self.last_message_count = 0  # Reset message count
        self.scroll_to_top()
        
        messages = self.chat_manager.get_messages()

        for role, content in messages[self.last_message_count:]:
            if role == 'user':
                widget = UserPrompt(self.chat_frame)
                widget.set_text(content.strip())
                widget.pack(padx=10, pady=5, anchor='e')
            elif role == 'assistant':
                widget = AssistantResponse(self.chat_frame)
                widget.set_text(content.strip())
                widget.pack(fill=tk.X, padx=10, pady=5, anchor='w')

        self.scroll_to_bottom()

    def send_message(self, prompt):
        # Save the new user message to the database
        self.chat_manager.add_message('user', prompt)

        prompt_widget = UserPrompt(self.chat_frame)
        prompt_widget.set_text(prompt)
        prompt_widget.pack(padx=10, pady=5, anchor='e')
        self.scroll_to_bottom()

        # Start a new assistant message in the database
        assistant_message_id = self.chat_manager.add_message('assistant', '')
        
        response_widget = AssistantResponse(self.chat_frame)
        response_widget.pack(fill=tk.X, padx=10, pady=5, anchor='w')
        self.scroll_to_bottom()

        response = self.model_manager.send_message(prompt)

        for chunk in response:
            chunk_content = chunk['message']['content']
            self.chat_manager.update_message(assistant_message_id, chunk_content)
            response_widget.insert_text(chunk_content)

        self.entry_field.message_sent()