import ollama
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.backend.chat_manager import ChatManager
from src.backend.system_manager import SystemManager

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
        self.current_model = None

        # Initialize Chat Manager
        self.chat_manager = ChatManager()

        try:
            self.current_model = self.list_models()[0]
        except IndexError:
            self.current_model = "No Models Installed"

    def available_models(self):
        return [("llama3.1:8b", 4.7), ("llama3.1:70b", 40), ("llama3.1:405b", 231), ("gemma2:2b", 1.6), ("gemma2:9b", 5.4), ("gemma2:27b", 16), ("mistral-nemo:12b", 7.1), ("mistral-large:123b", 69), ("mistral:7b", 4.1), ("phi3:3.8b", 2.2), ("phi3:14b", 7.9), ("codegemma:2b", 1.6), ("codegemma:7b", 5.0), ("llava:7b", 4.7), ("llava:13b", 8.0), ("llava:34b", 20)]
    
    def change_model(self, model_name):
        self.current_model = model_name

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
    
    def send_message(self, prompt):
        current_chat = self.chat_manager.get_current_chat()
        if not current_chat:
            print("No current chat selected.")
            return

        message_history = []

        # Initialize SystemManager to get the system message
        system_manager = SystemManager()
        system_file_path = os.path.join(system_manager.system_folder, system_manager.system_file)
        if os.path.exists(system_file_path):
            with open(system_file_path, 'r', encoding='utf-8') as system_file:
                system_message = system_file.read().strip()
                message_history.append({'role': 'system', 'content': system_message})

        # Read the current chat history from the database
        messages = self.chat_manager.get_messages()
        for role, content in messages:
            message_history.append({'role': role, 'content': content})

        # Add the new user prompt to the message history
        message_history.append({'role': 'user', 'content': prompt})

        # Send the message to the model
        return ollama.chat(
            model=self.current_model,
            messages=message_history,
            stream=True,
        )