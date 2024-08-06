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

        # Initialize download settings
        self.download_settings_file_name = 'download_settings.json'
        self.init_download_settings()

        # Initialize ui settings
        self.ui_settings_file_name = 'ui_settings.json'
        self.init_ui_settings()

        # Initialize system text settings
        self.agent_settings_file_name = 'agent_settings.json'
        self.init_agent_settings()

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
        
        self.default_model_settings = {
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9,
            "num_predict": 8000,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "repeat_penalty": 1.2,
            "repeat_last_n": 64,
            "mirostat": 0,
            "mirostat_tau": 5.0,
            "mirostat_eta": 0.1,
            "num_thread": 8,
            "num_ctx": 1024
        }

        self._ensure_file_exists(model_settings_file, self.default_model_settings)

    def get_model_settings(self):
        return self.read_settings(self.model_settings_file_name)

    def set_model_settings(self, new_settings):
        self.write_settings(self.model_settings_file_name, new_settings)

    # download settings methods
    def init_download_settings(self):
        download_settings_file = os.path.join(self.settings_folder, self.download_settings_file_name)

        self.default_download_settings = {
            "model": "llama3.1:8b",
            "available models": [
                ("llama3.1:8b", 4.7), 
                ("llama3.1:70b", 40), 
                ("llama3.1:405b", 231), 
                ("gemma2:2b", 1.6), 
                ("gemma2:9b", 5.4), 
                ("gemma2:27b", 16), 
                ("mistral-nemo:12b", 7.1), 
                ("mistral-large:123b", 69), 
                ("mistral:7b", 4.1), 
                ("phi3:3.8b", 2.2), 
                ("phi3:14b", 7.9), 
                ("codegemma:2b", 1.6), 
                ("codegemma:7b", 5.0), 
                ("llava:7b", 4.7), 
                ("llava:13b", 8.0), 
                ("llava:34b", 20)
            ]
        }

        self._ensure_file_exists(download_settings_file, self.default_download_settings)

    def get_download_settings(self):
        return self.read_settings(self.download_settings_file_name)
    
    def set_download_settings(self, new_settings):
        self.write_settings(self.download_settings_file_name, new_settings)

    # ui settings methods
    def init_ui_settings(self):
        ui_settings_file = os.path.join(self.settings_folder, self.ui_settings_file_name)
        
        self.default_ui_settings = {
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

        self._ensure_file_exists(ui_settings_file, self.default_ui_settings)

    def get_ui_settings(self):
        return self.read_settings(self.ui_settings_file_name)

    def set_ui_settings(self, new_settings):
        self.write_settings(self.ui_settings_file_name, new_settings)
    
    # agent settings methods
    def init_agent_settings(self):
        agent_settings_file = os.path.join(self.settings_folder, self.agent_settings_file_name)

        self.default_agent_settings = {
            "agent": "classic larry",
            "agents": {
                "classic larry": {
                    "name": "Larry",
                    "role": "a helpful AI assistant",
                    "personality": "fun, cheery",
                    "behaviors": [
                        "end every response with a comment saying you are always open to help and to ask you whatever",
                        "try to crack a couple jokes in every response"
                    ],
                },
                "coding larry": {
                    "name": "Larry",
                    "role": "an AI assistant to help with coding and debugging",
                    "personality": "informative, brief",
                    "behaviors": [
                        "add comments periodically describing attributes and methods",
                        "whenever editing code, add comments wherever you make changes/additions/removals"
                    ],
                }
            }
        }

        self._ensure_file_exists(agent_settings_file, self.default_agent_settings)
    
    def get_agent_settings(self):
        return self.read_settings(self.agent_settings_file_name)
    
    def set_agent_settings(self, new_settings):
        self.write_settings(self.agent_settings_file_name, new_settings)