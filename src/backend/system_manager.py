import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.backend.settings_manager import SettingsManager

class SystemManager:
    def __init__(self, system_folder='system', system_file='system.txt'):
        self.settings_manager = SettingsManager()

    def get_system_text(self):
        agent_settings = self.settings_manager.get_agent_settings()
        agent = agent_settings['agents'][agent_settings['agent']]

        system_text = f"This is who you are:\n"
        system_text += f"Name: {agent['name']}\n"
        system_text += f"Role: {agent['role']}\n"
        system_text += f"Personality: {agent['personality']}\n"
        system_text += "Behaviors:\n"

        for behavior in agent['behaviors']:
            system_text += f" - {behavior}\n"

        return system_text
    
    def list_agents(self):
        agent_settings = self.settings_manager.get_agent_settings()
        return list(agent_settings['agents'].keys())

    def get_current_agent(self):
        agent_settings = self.settings_manager.get_agent_settings()
        return agent_settings['agent']

    def change_agent(self, agent):
        agent_settings = self.settings_manager.get_agent_settings()
        if agent in agent_settings['agents']:
            agent_settings['agent'] = agent
            self.settings_manager.set_agent_settings(agent_settings)
        else:
            raise ValueError(f"Agent '{agent}' does not exist.")

if __name__ == "__main__":
    system_manager = SystemManager()
    print(system_manager.list_agents())