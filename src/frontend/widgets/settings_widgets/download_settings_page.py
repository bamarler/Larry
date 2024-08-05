import tkinter as tk
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.frontend.ui_constants import ui_constants
from src.frontend.widgets.settings_widgets.settings_page import SettingsPage
from src.backend.model_manager import ModelManager

FONT = ui_constants.FONT
FONTSIZE = ui_constants.FONTSIZE
BACKGROUND_COLOR = ui_constants.BACKGROUND_COLOR
HEADER_COLOR = ui_constants.HEADER_COLOR
ACCENT_COLOR = ui_constants.ACCENT_COLOR
TEXT_COLOR = ui_constants.TEXT_COLOR

class DownloadSettingsPage(SettingsPage):
    def __init__(self, parent):
        super().__init__(parent, "Manage Models")

        # Initialize Model Manager
        self.model_manager = ModelManager()
        
        # Create header label
        header_label = tk.Label(self.page, text="Manage Models", font=(FONT, FONTSIZE + 4, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        header_label.pack(pady=10)

        # Create the main frame for the lists
        list_frame = tk.Frame(self.page, bg=BACKGROUND_COLOR)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Downloaded models list
        downloaded_label = tk.Label(list_frame, text="Downloaded Models", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        downloaded_label.grid(row=0, column=0, padx=10, pady=5)

        self.downloaded_listbox = tk.Listbox(list_frame, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectbackground=ACCENT_COLOR, activestyle='none')
        self.downloaded_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.downloaded_listbox.bind("<<ListboxSelect>>", self.on_downloaded_select)

        # Available models list
        available_label = tk.Label(list_frame, text="Available Models", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        available_label.grid(row=0, column=1, padx=10, pady=5)

        self.available_listbox = tk.Listbox(list_frame, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectbackground=ACCENT_COLOR, activestyle='none')
        self.available_listbox.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.available_listbox.bind("<<ListboxSelect>>", self.on_available_select)

        # Configure grid weight for resizing
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_columnconfigure(1, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)

        # Frame for action buttons
        self.action_frame = tk.Frame(self.page, bg=BACKGROUND_COLOR)
        self.action_frame.pack(pady=10)

        self.action_button = tk.Button(self.action_frame, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        self.action_button.pack()

        # Status label
        self.status_label = tk.Label(self.page, text="Status: ", font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.status_label.pack(fill=tk.X, padx=5, pady=10)

        # Load models
        self.load_models()

    def load_models(self):
        self.downloaded_listbox.delete(0, tk.END)
        self.available_listbox.delete(0, tk.END)

        downloaded_models = self.model_manager.list_models()
        all_models = self.model_manager.available_models()

        for model in downloaded_models:
            self.downloaded_listbox.insert(tk.END, model)

        for model_name, model_size in all_models:
            if model_name not in downloaded_models:
                self.available_listbox.insert(tk.END, f"{model_name} ({model_size} GB)")

    def on_downloaded_select(self, event):
        self.action_button.config(text="Remove", command=self.remove_model)
        self.action_frame.pack(pady=10)
        
    def on_available_select(self, event):
        self.action_button.config(text="Install", command=self.install_model)
        self.action_frame.pack(pady=10)

    def install_model(self):
        selected_item = self.available_listbox.get(tk.ACTIVE)
        model_name = selected_item.split(" (")[0]
        install_thread = threading.Thread(target=self.thread_install, args=(model_name,))
        install_thread.start()
    
    def thread_install(self, model_name):
        ollama_pull = self.model_manager.install_model(model_name)

        for chunk in ollama_pull:
            status = f"status: {chunk['status']}"
            try:
                status = status + f" Completed: {chunk['completed']}/{chunk['total']}"
            except KeyError:
                pass
            self.status_label.config(text=status)
        
        self.status_label.config(text=f"{model_name} successfully installed")
        self.load_models()  # Update lists

    def remove_model(self):
        model_name = self.downloaded_listbox.get(tk.ACTIVE)
        remove_thread = threading.Thread(target=self.thread_remove, args=(model_name,))
        remove_thread.start()

    def thread_remove(self, model_name):
        ollama_remove = self.model_manager.remove_model(model_name)

        self.status_label.config(text=f"{ollama_remove['status']}")
        self.status_label.config(text=f"{model_name} successfully removed")
        self.load_models()  # Update lists