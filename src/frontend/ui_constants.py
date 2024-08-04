import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.backend.settings_manager import SettingsManager

class UIConstants:
    def __init__(self):
        self.settings_manager = SettingsManager()

        self.init_ui()
    
    def init_ui(self):
        ui_settings = self.settings_manager.get_ui_settings()

        self.FONT = ui_settings["font"]
        self.FONTSIZE = ui_settings["fontsize"]

        theme = ui_settings["theme"]
        themes = ui_settings["themes"]

        self.BACKGROUND_COLOR = themes[theme]["background_color"]
        self.HEADER_COLOR = themes[theme]["header_color"]
        self.ACCENT_COLOR = themes[theme]["accent_color"]
        self.TEXT_COLOR = themes[theme]["text_color"]

# Singleton instance of UIConstants
ui_constants = UIConstants()