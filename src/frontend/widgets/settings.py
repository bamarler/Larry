import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.backend.constants import *

class Settings(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack_propagate(False)  # Prevent the frame from resizing to its content
        
        self.sidebar_width = 200
        self.sidebar_frame = tk.Frame(self, width=self.sidebar_width)
        self.sidebar_frame.pack(side=tk.LEFT)

        self.main_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
