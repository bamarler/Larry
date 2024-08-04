import tkinter as tk
from tkhtmlview import HTMLLabel
import os
import sys
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.frontend.ui_constants import *

class AssistantResponse(tk.Frame):
    def __init__(self, parent, initial_text='', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(bg=BACKGROUND_COLOR)

        # Set up the HTMLLabel with initial text
        self.html_label = HTMLLabel(self, html=self.format_assistant_message(initial_text), background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
        self.html_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.html_label.fit_height()

        self.current_text = initial_text
        self.update_pending = False
    
    def get_text(self):
        return self.current_text

    def set_text(self, text):
        self.current_text = text
        self.schedule_update()
    
    def insert_text(self, text):
        self.set_text(self.current_text + text)
    
    def schedule_update(self):
        if not self.update_pending:
            self.update_pending = True
            self.after(100, self.update_html_label)
    
    def update_html_label(self):
        formatted_text = self.format_assistant_message(self.current_text)
        self.html_label.set_html(formatted_text)  # Update the HTML content
        self.html_label.fit_height()
        self.update_pending = False

    def format_assistant_message(self, message):
        """Format an assistant message for HTML display."""
        formatted_message = markdown.markdown(message, extensions=[TableExtension(), FencedCodeExtension()])
        return f"""
        <div style='text-align: left;'>
            <div style='display: inline-block; background-color: {BACKGROUND_COLOR}; border-radius: 10px; padding: 5px 10px; margin: 5px 10px 5px 0px; max-width: 70%; word-wrap: break-word; color: {TEXT_COLOR}; font-size: {FONTSIZE}px; white-space: pre-wrap;'>
                {formatted_message}
            </div>
        </div>
        """
