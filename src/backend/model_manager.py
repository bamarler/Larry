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
        response = ollama.chat(
            model=self.current_model,
            messages=message_history,
            stream=True,
        )

        # Save the new user message to the database
        self.chat_manager.add_message('user', prompt)

        # Start a new assistant message in the database
        assistant_message_id = self.chat_manager.add_message('assistant', '')

        # Append chunks to the assistant message in the database
        for chunk in response:
            message = chunk['message']['content']
            self.chat_manager.update_message(assistant_message_id, message)

        print("Message sent and response received.")

