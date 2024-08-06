import ollama
import threading
import queue
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.backend.chat_manager import ChatManager
from src.backend.system_manager import SystemManager
from src.backend.settings_manager import SettingsManager

class SingletonMeta(type):
    """
    A Singleton metaclass that ensures a class has only one instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class ModelManager(metaclass=SingletonMeta):
    def __init__(self):
        # Initialize Chat Manager
        self.chat_manager = ChatManager()

        # Initialize Settings Manager
        self.settings_manager = SettingsManager()

        # Initialize SystemManager to get the system message
        self.system_manager = SystemManager()

    def available_models(self):
        download_settings = self.settings_manager.get_download_settings()
        return download_settings["available models"]
    
    def add_model(self, model):
        download_settings = self.settings_manager.get_download_settings()
        download_settings["available models"].append(model)
        self.settings_manager.set_download_settings(download_settings)
    
    def get_current_model(self):
        download_settings = self.settings_manager.get_download_settings()
        return download_settings["model"]

    def change_model(self, model_name):
        download_settings = self.settings_manager.get_download_settings()
        download_settings["model"] = model_name
        self.settings_manager.set_download_settings(download_settings)

    def list_models(self):
        try:
            models = ollama.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def install_model(self, model_name):
        return ollama.pull(model_name, stream=True)
    
    def remove_model(self, model_name):
        return ollama.delete(model_name)
    
    def send_message(self, prompt, q):
        # Save the new user message to the database
        self.chat_manager.add_message('user', prompt)

        current_chat = self.chat_manager.get_current_chat()
        if not current_chat:
            print("No current chat selected.")
            return

        message_history = []

        # Read and add the system text
        system_text = self.system_manager.get_system_text()
        message_history.append({'role': 'system', 'content': system_text})

        # Read the current chat history from the database
        messages = self.chat_manager.get_messages()
        for role, content in messages:
            message_history.append({'role': role, 'content': content})

        # Add the new user prompt to the message history
        message_history.append({'role': 'user', 'content': prompt})

        model_settings = self.settings_manager.get_model_settings()

        # Send the message to the model
        response = ollama.chat(
            model=self.get_current_model(),
            messages=message_history,
            stream=True,
            options={
                "temperature":model_settings["temperature"],
                "top_k":model_settings["top_k"],
                "top_p":model_settings["top_p"],
                "num_predict":model_settings["num_predict"],
                "frequency_penalty":model_settings["frequency_penalty"],
                "presence_penalty":model_settings["presence_penalty"],
                "repeat_penalty":model_settings["repeat_penalty"],
                "repeat_last_n":model_settings["repeat_last_n"],
                "mirostat":model_settings["mirostat"],
                "mirostat_tau":model_settings["mirostat_tau"],
                "mirostat_eta":model_settings["mirostat_eta"],
                "num_thread":model_settings["num_thread"],
                "num_ctx":model_settings["num_ctx"],
            },
        )

        # save the model response to the database
        response_id = self.chat_manager.add_message('assistant', '')

        # Stream response to database and to the queue
        for chunk in response:
            chunk_content = chunk['message']['content']
            self.chat_manager.update_message(response_id, chunk_content)
            q.put(chunk_content)
        
        # Indicate stream completion
        q.put(None)
