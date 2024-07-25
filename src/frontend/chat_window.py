import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel
import ollama as larry
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from queue import Queue
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import re

# Colors and font settings
charcoal = '#2C2F33'
accent_purple = '#301b4d'  # Darker purple color for user prompts
off_white = '#d3d3d3'  # Off-white color for text
darker_gray = '#1E1E1E'  # Darker gray color
fontsize = 10
font = 'helvetica'

class ChatWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=charcoal)
        self.root = parent  # Reference to the root window

        # Create the HTML label for displaying the chat
        self.html_label = HTMLLabel(self, html="", width=80, height=40, background=charcoal, font=(font, fontsize))
        self.html_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        self.html_label.fit_height()
        self.html_label.yview_moveto(0)  # Ensure it starts at the top

        # Create a frame for the entry field and send button inside the chat frame
        self.entry_frame = tk.Frame(self, bg=charcoal)
        self.entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Create the entry field for user input
        self.entry_field = tk.Text(self.entry_frame, height=1, wrap=tk.WORD, font=(font, fontsize), bg=accent_purple, fg=off_white, bd=0)
        self.entry_field.pack(side=tk.LEFT, padx=(5, 0), pady=5, fill=tk.X, expand=True, ipadx=5, ipady=5)

        # Bind the Return key to the send_message function and Ctrl+Return to new line
        self.entry_field.bind("<Return>", self.send_message_event)
        self.entry_field.bind("<Control-Return>", self.new_line)

        # Create the send button
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, font=(font, fontsize), bg=charcoal, fg=off_white)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.full_response_html = ""
        self.chunk_buffer = ""
        self.current_response_html = ""

        self.queue = Queue()
        self.current_chat_file = None
        self.chat_folder = "chats"
        self.messages = []

        self.root.after(100, self.process_queue)

    def send_message_event(self, event=None):
        """Handle the event when Enter is pressed to send the message."""
        if event:
            if event.keysym == 'Return' and event.state & 0x4:  # Ctrl+Enter for new line
                return
            else:
                return self.send_message()  # Call send_message and return "break" to prevent default behavior
        return "break"

    def send_message(self, event=None):
        """Send the user's message."""
        user_input = self.entry_field.get("1.0", "end-1c").strip()
        if user_input:
            self.entry_field.delete("1.0", "end")

            # Write the user prompt and assistant tag into the .txt file
            with open(self.current_chat_file, "a", encoding="utf-8") as file:
                file.write(f"user: {user_input}\nassistant: ")

            # Append the user message to self.messages
            self.messages.append({'role': 'user', 'content': user_input})

            # Call update_chat_display to refresh the display
            self.update_chat_display()

            selected_model = self.model_var.get()  # Get the selected model

            # Disable the send button and entry field during processing
            self.send_button.config(state=tk.DISABLED)
            self.entry_field.config(state=tk.DISABLED)

            # Use a thread to handle the response fetching and streaming
            threading.Thread(target=self.fetch_response, args=(selected_model,)).start()

    def fetch_response(self, selected_model):
        """Fetch the response from the model."""
        response = larry.chat(
            model=selected_model,
            messages=self.messages,  # Use the message history
            stream=True,
        )

        # Reset buffer and current response for new response
        self.chunk_buffer = ""
        self.current_response_html = ""
        self.chunk_batch = []

        self.response_iterator = iter(response)
        self.process_chunks()

    def process_chunks(self):
        """Process chunks from the response iterator."""
        try:
            for _ in range(3):  # Adjust the batch size as needed
                chunk = next(self.response_iterator)
                self.chunk_batch.append(chunk['message']['content'])
                with open(self.current_chat_file, "a", encoding="utf-8") as file:
                    file.write(chunk['message']['content'])
            self.queue.put(self.chunk_batch)
            self.chunk_batch = []
            self.root.after(100, self.process_chunks)  # Small delay to avoid flickering
        except StopIteration:
            # Append the final response to self.messages
            with open(self.current_chat_file, "a", encoding="utf-8") as file:
                file.write("\n\n")
            self.messages.append({'role': 'assistant', 'content': self.chunk_buffer.strip()})

            # Re-enable the send button and entry field after processing
            self.send_button.config(state=tk.NORMAL)
            self.entry_field.config(state=tk.NORMAL)

            # Call update_chat_display to refresh the display
            self.update_chat_display()

    def display_chunks(self, chunks):
        """Display a batch of chunks in real-time."""
        for chunk in chunks:
            self.chunk_buffer += chunk

        # Update the chat display after writing chunks to the file
        self.update_chat_display()

    def update_chat_display(self):
        """Update the chat display based on the current chat file."""
        self.full_response_html = ""
        current_role = None  # Track the current role (user or assistant)

        try:
            with open(self.current_chat_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

            message_buffer = ""  # Buffer to accumulate message content

            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith("user:"):
                    # Process the previous message if any
                    if message_buffer:
                        if current_role == "user":
                            self.full_response_html += self.format_user_message(message_buffer)
                        elif current_role == "assistant":
                            self.full_response_html += self.format_assistant_message(message_buffer)
                        message_buffer = ""  # Reset the buffer for the next message

                    current_role = "user"
                    message_buffer += stripped_line[6:].strip()  # Collect message content without the tag
                elif stripped_line.startswith("assistant:"):
                    # Process the previous message if any
                    if message_buffer:
                        if current_role == "user":
                            self.full_response_html += self.format_user_message(message_buffer)
                        elif current_role == "assistant":
                            self.full_response_html += self.format_assistant_message(message_buffer)
                        message_buffer = ""  # Reset the buffer for the next message

                    current_role = "assistant"
                    message_buffer += stripped_line[11:].strip()  # Collect message content without the tag
                else:
                    message_buffer += "\n" + stripped_line  # Append to the buffer with a newline

            # Process any remaining message in the buffer
            if message_buffer:
                if current_role == "user":
                    self.full_response_html += self.format_user_message(message_buffer)
                elif current_role == "assistant":
                    self.full_response_html += self.format_assistant_message(message_buffer)

            self.html_label.set_html(self.full_response_html)
            self.html_label.yview_moveto(1.0)  # Scroll to the bottom after updating the display

        except Exception as e:
            print(f"Error updating chat display: {e}")

    def format_user_message(self, message):
        """Format a user message for HTML display."""
        return f"""
        <div style='text-align: right;'>
            <div style='display: inline-block; background-color: {accent_purple}; border-radius: 10px; padding: 5px 10px; margin: 5px 5px 5px auto; max-width: 70%; word-wrap: break-word; white-space: pre-wrap; color: {off_white}; font-size: {fontsize}px;'>
                {markdown.markdown(message, extensions=[TableExtension(), FencedCodeExtension()])}
            </div>
        </div>
        """

    def format_assistant_message(self, message):
        """Format an assistant message for HTML display."""
        return f"""
        <div style='text-align: left;'>
            <div style='display: inline-block; background-color: {charcoal}; border-radius: 10px; padding: 5px 10px; margin: 5px 10px 5px 0px; max-width: 70%; word-wrap: break-word; color: {off_white}; font-size: {fontsize}px;'>
                {markdown.markdown(message, extensions=[TableExtension(), FencedCodeExtension()])}
            </div>
        </div>
        """

    def process_queue(self):
        """Process the queue for updates."""
        try:
            while not self.queue.empty():
                chunk_batch = self.queue.get()
                self.display_chunks(chunk_batch)
        finally:
            self.root.after(100, self.process_queue)

    def new_line(self, event=None):
        """Insert a new line in the entry field when Ctrl+Return is pressed."""
        self.entry_field.insert(tk.INSERT, "\n")
        return "break"

    def resize_textbox(self, event=None):
        line_count = self.entry_field.index('end-1c').split('.')[0]
        self.entry_field.config(height=int(line_count))

    def set_current_chat_file(self, chat_file):
        self.current_chat_file = chat_file

    def set_messages(self, messages):
        self.messages = messages

    def initialize_queue(self):
        self.queue = Queue()
        self.after(100, self.process_queue)
