import tkinter as tk
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.frontend.ui_constants import *
from src.frontend.widgets.settings_widgets.settings_page import SettingsPage
from src.backend.model_manager import ModelManager

class DownloadSettingsPage(SettingsPage):
    def __init__(self, parent):
        super().__init__(parent, "Manage Models")

        # Initialize Model Manager
        self.model_manager = ModelManager()

        # Entry field for model name
        self.model_name_var = tk.StringVar()
        self.model_entry = tk.Entry(self.page, textvariable=self.model_name_var, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        self.model_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Install button
        self.install_button = tk.Button(self.page, text="Install", command=self.install_model, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        self.install_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Remove button
        self.remove_button = tk.Button(self.page, text="Remove", command=self.remove_model, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Status label
        self.status_label = tk.Label(self.page, text="Status: ", font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.status_label.pack(fill=tk.X, padx=5, pady=10)

    def install_model(self):
        install_thread = threading.Thread(target=self.thread_install)
        install_thread.start()
    
    def thread_install(self):
        model_name = self.model_name_var.get().strip()
        ollama_pull = self.model_manager.install_model(model_name)

        for chunk in ollama_pull:
            status = f"status: {chunk['status']}"
            try:
                status = status + f" Completed: {chunk['completed']}/{chunk['total']}"
            except KeyError:
                pass
            self.status_label.config(text=status)
        
        self.status_label.config(text=f"{model_name} successfully installed")

    def remove_model(self):
        remove_thread = threading.Thread(target=self.thread_remove)
        remove_thread.start()

    def thread_remove(self):
        model_name = self.model_name_var.get().strip()

        ollama_remove = self.model_manager.remove_model(model_name)

        self.status_label.config(text=f"{ollama_remove['status']}")
        self.status_label.config(text=f"{model_name} successfully removed")
            

