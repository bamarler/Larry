import os
import json

class SettingsManager:
    def __init__(self, settings_folder='settings'):
        self.settings_folder = settings_folder

        # Ensure the settings folder exists
        self._ensure_folder_exists()

        # Initialize model settings
        self.model_settings_file_name = 'model_settings.json'
        self.init_model_settings()

        # Initialize ui settings
        self.ui_settings_file_name = 'ui_settings.json'
        self.init_ui_settings()

    def _ensure_folder_exists(self):
        if not os.path.exists(self.settings_folder):
            os.makedirs(self.settings_folder)

    def _ensure_file_exists(self, filepath, default_content):
        if not os.path.exists(filepath):
            with open(filepath, 'w') as file:
                json.dump(default_content, file, indent=4)

    def read_settings(self, filename):
        filepath = os.path.join(self.settings_folder, filename)
        with open(filepath, 'r') as file:
            return json.load(file)

    def write_settings(self, filename, settings):
        filepath = os.path.join(self.settings_folder, filename)
        with open(filepath, 'w') as file:
            json.dump(settings, file, indent=4)

    # Model settings methods
    def init_model_settings(self):
        model_settings_file = os.path.join(self.settings_folder, self.model_settings_file_name)
        
        default_model_settings = {
            "general": {
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.9,
                "num_predict": 100,
                "frequency_penalty": 0.0
            },
            "advanced": {
                "presence_penalty": 0.0,
                "repeat_penalty": 1.2,
                "repeat_last_n": 64,
                "mirostat": 0,
                "mirostat_tau": 5.0,
                "mirostat_eta": 0.1,
                "num_thread": 8,
                "num_ctx": 1024
            }
        }

        self._ensure_file_exists(model_settings_file, default_model_settings)

    def get_model_settings(self):
        return self.read_settings(self.model_settings_file_name)

    def set_model_settings(self, new_settings):
        self.write_settings(self.model_settings_file_name, new_settings)

    # ui settings methods
    def init_ui_settings(self):
        ui_settings_file = os.path.join(self.settings_folder, self.ui_settings_file_name)
        
        default_ui_settings = {
            "font": "helvetica",
            "fontsize": 10,
            "theme": "dark",
            "themes": {
                "dark": {
                    "background_color": "#2C2F33",
                    "header_color": "#1E1E1E",
                    "accent_color": "#301b4d",
                    "text_color": "#d3d3d3"
                },
                "light": {
                    "background_color": "#FFFFFF",
                    "header_color": "#F0F0F0",
                    "accent_color": "#007BFF",
                    "text_color": "#000000"
                }
            }
        }

        self._ensure_file_exists(ui_settings_file, default_ui_settings)

    def get_ui_settings(self):
        return self.read_settings(self.ui_settings_file_name)

    def set_ui_settings(self, new_settings):
        self.write_settings(self.ui_settings_file_name, new_settings)