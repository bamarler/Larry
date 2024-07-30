import os
import glob

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
    def __init__(self, chat_folder='chats'):
        self.chat_folder = chat_folder
        if not os.path.exists(self.chat_folder):
            os.makedirs(self.chat_folder)
        self.current_chat = None

    def create_new_chat(self):
        chat_name = f"Untitled Chat {len(glob.glob(os.path.join(self.chat_folder, 'Untitled Chat*.txt'))) + 1}"
        chat_path = os.path.join(self.chat_folder, f"{chat_name}.txt")
        if not os.path.exists(chat_path):
            with open(chat_path, 'w') as chat_file:
                chat_file.write("")  # Create an empty file
        self.change_chat(chat_name)

    def change_chat(self, chat_name):
        self.current_chat = chat_name

    def list_chats(self):
        all_chats = [os.path.splitext(chat)[0] for chat in os.listdir(self.chat_folder) if chat.endswith('.txt')]
        return [chat for chat in all_chats if chat != self.current_chat]

    def get_current_chat(self):
        return self.current_chat

    def get_current_chat_path(self):
        if self.current_chat:
            return os.path.join(self.chat_folder, f"{self.current_chat}.txt")
        else:
            return None
    
    def remove_chat(self):
        if self.current_chat:
            current_chat_path = self.get_current_chat_path()
            if current_chat_path and os.path.exists(current_chat_path):
                os.remove(current_chat_path)
            
            all_chats = self.list_chats()
            if all_chats:
                self.change_chat(all_chats[0])
            else:
                self.create_new_chat()