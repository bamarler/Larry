import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.frontend.ui_constants import *
from src.backend.chat_manager import ChatManager
from src.backend.model_manager import ModelManager
from src.frontend.widgets.chat_widgets.entry_field import EntryField
from src.frontend.widgets.chat_widgets.user_prompt import UserPrompt
from src.frontend.widgets.chat_widgets.assistant_response import AssistantResponse

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
        self.entry_field = EntryField(self)
        self.entry_field.pack(fill=tk.X, side=tk.BOTTOM, pady=10, padx=10)

        # Manage Chat Feed
        self.chat_display_frame = tk.Frame(self, bg=BACKGROUND_COLOR)  # Frame to hold chat widgets
        self.chat_display_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_display_frame, troughcolor=BACKGROUND_COLOR, bg=ACCENT_COLOR)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_canvas = tk.Canvas(self.chat_display_frame, bg=BACKGROUND_COLOR, yscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.chat_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.chat_canvas.yview)

        self.chat_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.chat_canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self.chat_canvas.bind_all("<Button-5>", self._on_mouse_wheel)

        self.chat_frame = tk.Frame(self.chat_canvas, bg=BACKGROUND_COLOR)
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor='nw')

        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        
        self.refresh()

        # Create new chat
        self.create_new_chat()

        # Initialize chat feed updating
        self.init_chat_monitoring()

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
            self.refresh()
            # Clear the canvas of any widgets
            for widget in self.chat_frame.winfo_children():
                widget.pack_forget()
                widget.destroy()
            self.last_message_count = 0  # Reset message count
            self.scroll_to_top()
            self.update_chat_feed()

    def create_new_chat(self):
        self.chat_manager.create_new_chat()
        self.selected_chat.set(self.chat_manager.get_current_chat())
        self.refresh()
    
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


    def init_chat_monitoring(self):
        self.update_chat_feed()
        threading.Thread(target=self.update_chat_feed_continuously, daemon=True).start()

    def update_chat_feed(self):
        messages = self.chat_manager.get_messages()
        new_messages = messages[self.last_message_count:]

        if new_messages:
            buffer_content = ""
            buffer_widgets = []

            for role, content in new_messages:
                if role == 'user':
                    widget = UserPrompt(self.chat_frame)
                    widget.set_text(content.strip())
                    buffer_widgets.append((widget, {'padx': 10, 'pady': 5, 'anchor': 'e'}))
                elif role == 'assistant':
                    widget = AssistantResponse(self.chat_frame)
                    widget.set_text(content.strip())
                    buffer_widgets.append((widget, {'fill': tk.X, 'padx': 10, 'pady': 5, 'anchor': 'w'}))
                buffer_content += content.strip() + "\n"

            # Apply the buffered updates to the UI
            for widget, options in buffer_widgets:
                widget.pack(**options)

            self.last_message_count = len(messages)
            self.scroll_to_bottom()
        elif not self.entry_field.ready_to_send and messages:
            last_role, last_content = messages[-1]
            last_widget = self.chat_frame.winfo_children()[-1]  # Get the last widget

            last_widget.set_text(last_content.strip())
            self.scroll_to_bottom()

    def update_chat_feed_continuously(self):
        while True:
            self.update_chat_feed()
            time.sleep(0.1)  # Add a small delay to reduce CPU usage