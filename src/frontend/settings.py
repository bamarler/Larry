import tkinter as tk
from tkinter import ttk
import ollama as larry

# Colors and font settings
darker_gray = '#1E1E1E'
off_white = '#d3d3d3'
font = 'helvetica'
fontsize = 10

class SettingsPage(tk.Frame):
    def __init__(self, parent, update_model_list_callback):
        super().__init__(parent, bg=darker_gray)

        self.update_model_list_callback = update_model_list_callback

        # Back button
        self.back_button = tk.Button(self, text="Back", command=self.show_chat_page, bg=darker_gray, fg=off_white, bd=0, font=(font, fontsize))
        self.back_button.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.close_window, bg=darker_gray, fg=off_white, bd=0, font=(font, fontsize))
        self.quit_button.pack(side=tk.BOTTOM, pady=20)

        # Add dropdown menu of models
        self.models = larry.list()['models']
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(self, textvariable=self.model_var, state='readonly', font=(font, fontsize))
        self.model_dropdown.pack(pady=10)
        self.update_model_list()

    def update_model_list(self):
        models = larry.list()['models']
        model_names = [model['name'] for model in models]
        self.model_dropdown['values'] = model_names

    def show_chat_page(self):
        self.pack_forget()
        self.master.show_chat_page()

    def close_window(self):
        self.master.close_window()
