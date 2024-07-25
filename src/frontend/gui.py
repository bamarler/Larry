import tkinter as tk
from tkinter import ttk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.backend.constants import *
from src.frontend.widgets.settings import Settings
from src.frontend.widgets.chat_window import ChatWindow

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App")

        # Disable window bar and prevent resizing vertically
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)  # Keep the window always on top

        # Get screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Assume a typical taskbar height (50 pixels)
        taskbar_height = 48

        # Set initial window dimensions and position
        self.window_width = self.screen_width // 3
        self.window_height = screen_height - taskbar_height
        self.x_position = self.screen_width - self.window_width
        y_position = 0

        # Set geometry of the window and allow width resizing
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{y_position}")
        self.root.resizable(True, False)  # Enable width resizing, disable height resizing

        # Create a frame for the top buttons
        self.top_frame = tk.Frame(self.root, bg=HEADER_COLOR)
        self.top_frame.pack(fill=tk.X)

        # Add a button to open the settings
        self.settings_button = tk.Button(self.top_frame, text="⚙", command=self.toggle_settings, bg=HEADER_COLOR, fg=TEXT_COLOR, bd=0, font=(FONT, FONTSIZE))
        self.settings_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Add a button to close app
        self.new_chat_button = tk.Button(self.top_frame, text="✖", command=self.close_window, bg=HEADER_COLOR, fg=TEXT_COLOR, bd=0, font=(FONT, FONTSIZE))
        self.new_chat_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Add a button to switch sides
        self.new_chat_button = tk.Button(self.top_frame, text="⇆", command=self.toggle_side, bg=HEADER_COLOR, fg=TEXT_COLOR, bd=0, font=(FONT, FONTSIZE))
        self.new_chat_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create a frame container to hold the main content
        self.frame_container = tk.Frame(self.root, bg=ACCENT_COLOR)
        self.frame_container.pack(fill=tk.BOTH, expand=True)

        # Create the chat window widget
        self.chat_window = ChatWindow(self.frame_container)
        self.chat_window.pack(fill=tk.BOTH, expand=True)

        # Create the settings widget
        self.settings = Settings(self.frame_container)
        self.settings_open = False

        self.side = "right"
        self.enable_edge_resizing()
        self.root.bind("<Escape>", lambda event: self.close_window())

    def close_window(self):
        self.root.destroy()

    def enable_edge_resizing(self):
        border_width = 10  # Width of the resize border area

        def start_resize(event):
            self.init_x = event.x_root
            self.init_width = self.root.winfo_width()
            self.init_x_position = self.root.winfo_x()

        def perform_resize(event):
            delta_x = event.x_root - self.init_x

            if self.side == "right":
                new_width = self.init_width - delta_x
                new_x_position = self.init_x_position + delta_x
            else:  # side == "left"
                new_width = self.init_width + delta_x
                new_x_position = self.init_x_position

            if self.screen_width // 2 > new_width > self.screen_width // 4:  # Minimum window width
                self.window_width = new_width
                self.root.geometry(f"{new_width}x{self.window_height}+{new_x_position}+0")
        
        def on_mouse_move(event):
            x = event.x
            y = event.y
            
            if (self.side == "right" and x < border_width) or (self.side == "left" and x > self.root.winfo_width() - border_width):
                self.root.config(cursor="sb_h_double_arrow")
                self.root.bind("<Button-1>", start_resize)
                self.root.bind("<B1-Motion>", perform_resize)
            else:
                self.root.config(cursor="")
                self.root.unbind("<Button-1>")
                self.root.unbind("<B1-Motion>")

        self.root.bind("<Motion>", on_mouse_move)

    def toggle_settings(self):
        if self.settings_open:
            self.settings.pack_forget()
            self.settings_open = False
            self.settings_button.config(text="⚙")
            self.chat_window.pack(fill=tk.BOTH, expand=True)
        else:
            self.chat_window.pack_forget()
            self.settings.pack(fill=tk.BOTH, expand=True)
            self.settings_open = True
            self.settings_button.config(text="<<")
    
    def toggle_side(self):
        if self.side == "right":
            self.side = "left"
            self.x_position = 0
        else:
            self.side = "right"
            self.x_position = self.screen_width - self.window_width

        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+0")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
