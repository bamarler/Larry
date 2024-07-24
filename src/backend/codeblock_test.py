import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel
import pyperclip

# Colors and font settings
charcoal = '#2C2F33'
accent_purple = '#301b4d'  # Darker purple color for user prompts
off_white = '#d3d3d3'  # Off-white color for text
darker_gray = '#1E1E1E'  # Darker gray color
fontsize = 10
font = 'helvetica'

class CodeBlock(tk.Frame):
    def __init__(self, master, code, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.code = code

        self.html_label = HTMLLabel(self, html=self.generate_html(), background=charcoal, font=(font, fontsize))
        self.html_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.copy_button = tk.Button(self, text="Copy", command=self.copy_code, bg=accent_purple, fg=off_white, font=(font, fontsize))
        self.copy_button.pack(side=tk.RIGHT, padx=5)

    def generate_html(self):
        html_code = self.code.replace(" ", "&nbsp;").replace("\n", "<br>")
        return f"""
        <div style='padding: 10px; background-color: {charcoal}; border-radius: 5px; color: {off_white}; font-family: {font}; font-size: {fontsize}px;'>
            <pre>{html_code}</pre>
        </div>
        """

    def copy_code(self):
        pyperclip.copy(self.code)
        self.copy_button.config(text="Copied!")

def show_code_block(master, code):
    code_block = CodeBlock(master, code, bg=charcoal)
    code_block.pack(fill=tk.BOTH, padx=10, pady=10)

# Sample usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Code Block Example")
    root.geometry("600x400")
    root.configure(bg=charcoal)

    sample_code = """import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel
import pyperclip

# Colors and font settings
charcoal = '#2C2F33'
accent_purple = '#301b4d'  # Darker purple color for user prompts
off_white = '#d3d3d3'  # Off-white color for text
darker_gray = '#1E1E1E'  # Darker gray color
fontsize = 10
font = 'helvetica'

class CodeBlock(tk.Frame):
    def __init__(self, master, code, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.code = code

        self.html_label = HTMLLabel(self, html=self.generate_html(), background=charcoal, font=(font, fontsize))
        self.html_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.copy_button = tk.Button(self, text="Copy", command=self.copy_code, bg=accent_purple, fg=off_white, font=(font, fontsize))
        self.copy_button.pack(side=tk.RIGHT, padx=5)

    def copy_code(self):
        pyperclip.copy(self.code)
        self.copy_button.config(text="Copied!")
"""

    show_code_block(root, sample_code)

    root.mainloop()
