import os

class SystemManager:
    def __init__(self, system_folder='system', system_file='system.txt'):
        self.system_folder = system_folder
        self.system_file = system_file
        self.initialize_system()

    def initialize_system(self):
        if not os.path.exists(self.system_folder):
            os.makedirs(self.system_folder)
        
        system_file_path = os.path.join(self.system_folder, self.system_file)
        if not os.path.exists(system_file_path):
            with open(system_file_path, 'w') as file:
                file.write("You are Larry, a helpful AI assistant\n")