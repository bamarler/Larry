import tkinter as tk
from tkhtmlview import HTMLLabel

# Colors and font settings
BACKGROUND_COLOR = '#2C2F33'
HEADER_COLOR = '#1E1E1E'
ACCENT_COLOR = '#301b4d' 
TEXT_COLOR = '#d3d3d3'

FONTSIZE = 10
FONT = 'helvetica'

class SimpleHTMLFrame(tk.Frame):
    def __init__(self, parent, html_content="", **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg=ACCENT_COLOR)
        
        self.text_window = HTMLLabel(self, html=html_content, background=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT, FONTSIZE))
        self.text_window.pack(fill="x", expand=True)

        self.text_window.fit_height()

# Sample usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple HTML Frame Example")
    root.geometry("400x300")
    root.configure(bg=BACKGROUND_COLOR)

    html_content = """
    <h1 style='color:{};'>Welcome to the HTML Frame</h1>
    <p style='color:{};'>This is a sample paragraph with <b>bold</b> and <i>italic</i> text.</p>
    <a style='color:{};' href="https://www.example.com">Visit Example</a>
    """.format(TEXT_COLOR, TEXT_COLOR, TEXT_COLOR)
    
    frame = SimpleHTMLFrame(root, html_content)
    frame.pack(fill="both", expand=True)

    root.mainloop()
