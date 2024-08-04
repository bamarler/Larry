import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from database_manager import DatabaseManager

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

class ChatManager(metaclass=SingletonMeta):
    def __init__(self, db_path='chats.db'):
        self.db_manager = DatabaseManager(db_path)
        self.current_chat_id = None
        self.current_chat_name = None

    def create_new_chat(self):
        if self.current_chat_name != None:
            # Check if the current chat is empty before switching
            if not self.get_messages():
                return self.current_chat_name
        
        chat_name = f"Untitled Chat {len(self.db_manager.list_chats()) + 1}"
        self.db_manager.create_chat(chat_name)
        return chat_name

    def change_chat(self, chat_name):
        if self.current_chat_id:
            # Check if the current chat is empty before switching
            if not self.get_messages():
                self.remove_chat()
        chat_id = self.db_manager.get_chat_id(chat_name)
        if chat_id:
            self.current_chat_id = chat_id[0]
            self.current_chat_name = chat_name

    def list_chats(self):
        return self.db_manager.list_chats()
    
    def get_current_chat(self):
        return self.current_chat_name

    def get_current_chat_id(self):
        return self.current_chat_id

    def add_message(self, role, content):
        if self.current_chat_id:
            return self.db_manager.add_message(self.current_chat_id, role, content)

    def update_message(self, message_id, new_content):
        self.db_manager.update_message(message_id, new_content)

    def get_messages(self):
        if self.current_chat_id:
            return self.db_manager.get_messages(self.current_chat_id)
        return []

    def remove_chat(self):
        if self.current_chat_id:
            current_chat_index = self.db_manager.list_chats().index(self.current_chat_name)
            self.db_manager.remove_chat(self.current_chat_id)
            chat_list = self.list_chats()
            if chat_list:
                new_chat_index = min(current_chat_index, len(chat_list) - 1)
                next_chat_name = chat_list[new_chat_index]
                next_chat_id = self.db_manager.get_chat_id(next_chat_name)[0]
                self.current_chat_id = next_chat_id
                self.current_chat_name = next_chat_name
            else:
                self.current_chat_id = None
                self.current_chat_name = None