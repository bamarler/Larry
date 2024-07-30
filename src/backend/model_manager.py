import ollama
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.backend.chat_manager import ChatManager
from src.backend.system_manager import SystemManager

class ModelManager:
    def __init__(self):
        self.current_model = None

        # Initialize Chat Manager
        self.chat_manager = ChatManager()

        try:
            self.current_model = self.list_models()[0]
        except IndexError:
            self.current_model = "No Models Installed"

    def change_model(self, model_name):
        self.current_model = model_name

    def list_models(self):
        try:
            models = ollama.list()
            model_names = [model['name'] for model in models['models']]
            return [model for model in model_names if model != self.current_model]
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

        chat_file_path = self.chat_manager.get_current_chat_path()
        message_history = []

        # Initialize SystemManager to get the system message
        system_manager = SystemManager()
        system_file_path = os.path.join(system_manager.system_folder, system_manager.system_file)
        if os.path.exists(system_file_path):
            with open(system_file_path, 'r', encoding='utf-8') as system_file:
                system_message = system_file.read().strip()
                message_history.append({'role': 'system', 'content': system_message})

        # Read the current chat history
        if os.path.exists(chat_file_path):
            with open(chat_file_path, 'r', encoding='utf-8') as chat_file:
                lines = chat_file.readlines()
                role = None
                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line.startswith("user:"):
                        role = "user"
                        content = stripped_line[5:].strip()
                    elif stripped_line.startswith("assistant:"):
                        role = "assistant"
                        content = stripped_line[10:].strip()
                    else:
                        content = stripped_line

                    if role and content:
                        message_history.append({'role': role, 'content': content})

        # Add the new user prompt to the message history
        message_history.append({'role': 'user', 'content': prompt})

        # Send the message to the model
        response = ollama.chat(
            model=self.current_model,
            messages=message_history,
            stream=True,
        )

        # Write the new prompt and response to the chat file
        with open(chat_file_path, 'a', encoding='utf-8') as chat_file:
            chat_file.write(f"\n\nuser: {prompt}\nassistant: ")
        for chunk in response:
            message = chunk['message']['content']
            with open(chat_file_path, 'a', encoding='utf-8') as chat_file:
                chat_file.write(f"{message}")

        print("Message sent and response received.")

