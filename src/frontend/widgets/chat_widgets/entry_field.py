import tkinter as tk
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.frontend.ui_constants import *
from src.backend.model_manager import ModelManager

class EntryField(tk.Frame):
    def __init__(self, parent, send_function):
        super().__init__(parent, bg=ACCENT_COLOR)
        
        self.send_function = send_function

        # Initialize Model Manager
        self.model_manager = ModelManager()

        # Create a frame to hold the entry field and the button
        self.entry_frame = tk.Frame(self, bg=ACCENT_COLOR)
        self.entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the entry field
        self.entry = tk.Text(self.entry_frame, wrap=tk.WORD, font=(FONT, FONTSIZE), bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0, height=1)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bind the Return key to the send_message function and Ctrl+Return to new line
        self.entry.bind("<Return>", self.send_message_event)
        self.entry.bind("<Control-Return>", self.new_line)
        self.entry.bind("<Shift-Return>", self.new_line)
        self.entry.bind("<KeyRelease>", self.check_line_width)  # Bind the new method to KeyRelease
        self.entry.bind("<KeyRelease>", self.resize_entry_field)

        # Create the send button
        self.send_button = tk.Button(self, text="►", command=self.send_message, font=(FONT, FONTSIZE), bg=TEXT_COLOR, fg=HEADER_COLOR, bd=0)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor='se')

        # Boolean to enable send
        self.ready_to_send = True

    def send_message_event(self, event=None):
        """Handle the event when Enter is pressed to send the message."""
        if event:
            if event.keysym == 'Return' and event.state & 0x4:  # Ctrl+Enter for new line
                return
            else:
                return self.send_message()  # Call send_message and return "break" to prevent default behavior
        return "break"

    def send_message(self):
        """Send the user's message."""
        user_input = self.entry.get("1.0", "end-1c").strip()
        if user_input and self.ready_to_send:
            self.entry.delete("1.0", "end")
            self.ready_to_send = False
            self.send_button.config(text="◼")
            
            install_thread = threading.Thread(target=lambda: self.send_function(user_input))
            install_thread.start()
            
    def message_sent(self):
        self.send_button.config(text="►")
        self.ready_to_send = True

    def new_line(self, event=None):
        """Insert a new line in the entry field when Ctrl+Return is pressed."""
        self.entry.insert(tk.INSERT, "\n")
        return "break"

    def resize_entry_field(self, event=None):
        """Resize the entry field based on the content."""
        line_count = int(self.entry.index('end-1c').split('.')[0])

        max_lines = 15  # Max height of the entry field in lines
        
        if line_count <= max_lines:
            self.entry.config(height=line_count)
        else:
            self.entry.config(height=max_lines)

    def check_line_width(self, event=None):
        """Check if the width of the text on the current line exceeds the width of the field, and if so, insert a newline."""
        # Get the current line index
        current_index = self.entry.index(tk.INSERT)
        line_start = f"{current_index.split('.')[0]}.0"
        line_end = self.entry.index(f"{current_index.split('.')[0]}.end")

        # Get the width of the text on the current line
        line_text = self.entry.get(line_start, line_end)

        # Calculate the pixel width of the text
        pixel_width = self.entry.bbox(line_start)[2]

        # Get the pixel width of the text widget
        widget_width = self.entry.winfo_width()

        # Insert a newline if the text width exceeds the widget width
        if pixel_width + 1 > widget_width:
            self.entry.insert(line_end, "\n")