import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel
import ollama as larry
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from queue import Queue
import threading
import time
import os
import glob
from tkinter import filedialog
import pyperclip
import re

# Colors and font settings
charcoal = '#2C2F33'
accent_purple = '#301b4d'  # Darker purple color for user prompts
off_white = '#d3d3d3'  # Off-white color for text
darker_gray = '#1E1E1E'  # Darker gray color
fontsize = 10
font = 'helvetica'

class ChatWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat with Larry")

        # Initialization for system folder and functions.txt
        self.system_folder = "system"
        self.system_file = os.path.join(self.system_folder, "functions.txt")
        self.messages = []  # Initialize messages list
        self.initialize_system_file()

        # Disable window bar and prevent resizing/moving
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)  # Keep the window always on top

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Assume a typical taskbar height (50 pixels)
        taskbar_height = 50

        # Set window dimensions and position
        window_width = screen_width // 4
        window_height = screen_height - taskbar_height
        x_position = screen_width - window_width
        y_position = 0

        # Set geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Create a frame for the top buttons
        self.top_frame = tk.Frame(self.root, bg=darker_gray)
        self.top_frame.pack(fill=tk.X)

        # Create a refresh button with text inside the top frame
        self.refresh_button = tk.Button(self.top_frame, text="⟳", command=self.refresh, font=(font, fontsize), bg=darker_gray, fg=off_white, bd=0)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Add a dropdown menu for chat selection
        self.selected_chat = tk.StringVar()
        self.chat_dropdown = ttk.Combobox(self.top_frame, textvariable=self.selected_chat, state='readonly', font=(font, fontsize))
        self.chat_dropdown.pack(side=tk.LEFT, padx=10)
        self.chat_dropdown.bind("<<ComboboxSelected>>", self.change_chat)

        # Create a settings button with text inside the top frame
        self.settings_button = tk.Button(self.top_frame, text="⚙", command=self.show_settings_page, font=(font, fontsize), bg=darker_gray, fg=off_white, bd=0)
        self.settings_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Add a new chat button
        self.new_chat_button = tk.Button(self.top_frame, text="+", command=self.new_chat, font=(font, fontsize), bg=darker_gray, fg=off_white, bd=0)
        self.new_chat_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Initialize chat frame
        self.chat_frame = tk.Frame(self.root, bg=charcoal)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        # Create the HTML label for displaying the chat
        self.html_label = HTMLLabel(self.chat_frame, html="", width=80, height=40, background=charcoal, font=(font, fontsize))
        self.html_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        self.html_label.fit_height()
        self.html_label.yview_moveto(0)  # Ensure it starts at the top

        # Create a frame for the entry field and send button inside the chat frame
        self.entry_frame = tk.Frame(self.chat_frame, bg=charcoal)
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

        # Set the initial theme to dark
        self.root.config(bg=charcoal)

        self.full_response_html = ""
        self.chunk_buffer = ""
        self.current_response_html = ""

        # Auto-resize the text box
        self.entry_field.bind("<KeyRelease>", self.resize_textbox)

        self.init_settings_page()

        # Ensure chat folder exists
        self.chat_folder = "chats"
        self.current_chat_file = None
        self.full_response_html = ""

        self.new_chat()

        # Queue for communication between threads
        self.queue = Queue()

        # Periodically check the queue for updates
        self.root.after(100, self.process_queue)
        
        # Update the model list
        self.update_model_list()

    def initialize_system_file(self):
        """Initialize the system folder and functions.txt if they don't exist, and read system file content."""
        if not os.path.exists(self.system_folder):
            os.makedirs(self.system_folder)
        if not os.path.exists(self.system_file):
            with open(self.system_file, "w", encoding="utf-8") as file:
                file.write("You are Larry, a helpful AI assistant\n")
        
        # Read system file content and add to messages
        with open(self.system_file, "r", encoding="utf-8") as file:
            system_content = file.read().strip()
            self.messages = [{"role": "system", "content": system_content}]

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

    def close_window(self):
        self.root.destroy()
    
    def init_settings_page(self):
        self.settings_frame = tk.Frame(self.root, bg=charcoal)
        
        # Back button
        self.back_button = tk.Button(self.settings_frame, text="Back", command=self.show_chat_page, bg=darker_gray, fg=off_white, bd=0, font=(font, fontsize))
        self.back_button.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)
        
        # Quit button
        self.quit_button = tk.Button(self.settings_frame, text="Quit", command=self.close_window, bg=darker_gray, fg=off_white, bd=0, font=(font, fontsize))
        self.quit_button.pack(side=tk.BOTTOM, pady=20)

        # Add dropdown menu of models
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.model_var, state='readonly', font=(font, fontsize))
        self.model_dropdown.pack(pady=10)

        self.update_model_list()

    def update_model_list(self):
        """Update the model list in the dropdown menu without resetting the selected model."""
        models = larry.list()  # Acquire the list of available models
        model_names = [model['name'] for model in models['models']]  # Extract model names from the dictionary
        current_selection = self.model_var.get()  # Save the current selection
        self.model_dropdown['values'] = model_names
        if current_selection in model_names:
            self.model_var.set(current_selection)  # Restore the current selection
        elif model_names:
            self.model_var.set(model_names[0])  # Set the first model as default if current selection is invalid

    def show_settings_page(self):
        self.chat_frame.pack_forget()
        self.entry_frame.pack_forget()
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

    def show_chat_page(self):
        self.settings_frame.pack_forget()
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        self.entry_frame.pack(fill=tk.X, padx=10, pady=5)
        self.html_label.yview_moveto(0)  # Ensure it starts at the top

    def update_chat_list(self):
        chat_files = glob.glob(os.path.join(self.chat_folder, "*.txt"))
        if not chat_files:
            self.new_chat()
            return
        chat_names = [os.path.basename(chat_file).replace(".txt", "") for chat_file in chat_files]
        self.chat_dropdown['values'] = chat_names

    def save_chat_history(self):
        if not self.current_chat_file:
            base_name = "Untitled Chat"
            count = len(glob.glob(os.path.join(self.chat_folder, f"{base_name}*.txt"))) + 1
            self.current_chat_file = os.path.join(self.chat_folder, f"{base_name} {count}.txt")

        with open(self.current_chat_file, "w", encoding="utf-8") as file:
            for message in self.messages:
                file.write(f"{message['role']}: {message['content']}\n")

    def load_chat_history(self):
        if not self.current_chat_file:
            return

        with open(self.current_chat_file, "r", encoding="utf-8") as file:
            content = file.read()

        self.messages = []
        self.initialize_system_file()

        # Split the content by "assistant: " to differentiate between user and assistant messages
        parts = content.split("\nassistant: ")

        for part in parts:
            if "user: " in part:
                user_part, assistant_part = part.split("user: ", 1)
                if user_part.strip():
                    self.messages.append({'role': 'assistant', 'content': user_part.strip()})
                self.messages.append({'role': 'user', 'content': assistant_part.strip()})

        # Handle the case where the final assistant response is not loaded
        if not content.endswith("\n"):
            self.messages.append({'role': 'assistant', 'content': parts[-1].strip()})

        self.update_chat_display()

    def change_chat(self, event=None):
        selected_chat = self.selected_chat.get()
        if selected_chat:
            self.current_chat_file = os.path.join(self.chat_folder, f"{selected_chat}.txt")
            self.load_chat_history()
            self.update_chat_display()  # Ensure the chat display is updated and auto-scrolls to the bottom

    def new_chat(self):
        self.messages = []
        self.initialize_system_file()
        self.full_response_html = ""
        self.current_chat_file = None
        self.html_label.set_html("")
        self.selected_chat.set(f"Untitled Chat {len(glob.glob(os.path.join(self.chat_folder, 'Untitled Chat*.txt'))) + 1}")
        self.save_chat_history()
        self.update_chat_list()

    def save_chat_history_and_open(self):
        self.save_chat_history()
        self.change_chat()

    def refresh(self):
        self.update_chat_list()
        self.update_model_list()
        self.load_chat_history()
        self.update_chat_display()


# Create and run the chat window
chat_window = ChatWindow()
chat_window.show_chat_page()
chat_window.root.mainloop()

