import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.frontend.ui_constants import *
from src.frontend.widgets.settings_widgets.settings_page import SettingsPage

class TemplateSettingsPage(SettingsPage):
    def __init__(self, parent):
        super().__init__(parent, "Template Page")