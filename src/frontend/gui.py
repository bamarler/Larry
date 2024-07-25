import tkinter as tk

# Colors and font settings
charcoal = '#2C2F33'
off_white = '#d3d3d3'
darker_gray = '#1E1E1E'
fontsize = 10
font = 'helvetica'

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App")

        # Disable window bar and prevent resizing vertically
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)  # Keep the window always on top

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Assume a typical taskbar height (50 pixels)
        taskbar_height = 50

        # Set initial window dimensions and position
        self.window_width = screen_width // 4
        self.window_height = screen_height - taskbar_height
        x_position = screen_width - self.window_width
        y_position = 0

        # Set geometry of the window and allow width resizing
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")
        self.root.resizable(True, False)  # Enable width resizing, disable height resizing

        # Create a frame for the top buttons
        self.top_frame = tk.Frame(self.root, bg=darker_gray)
        self.top_frame.pack(fill=tk.X)

        # Add a button to close the window
        self.close_button = tk.Button(self.top_frame, text="X", command=self.close_window, bg=darker_gray, fg=off_white, bd=0, font=(font, fontsize))
        self.close_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create a frame container to hold the main content
        self.frame_container = tk.Frame(self.root, bg=charcoal)
        self.frame_container.pack(fill=tk.BOTH, expand=True)

        self.enable_resizing()

    def close_window(self):
        self.root.destroy()

    def enable_resizing(self):
        def start_resize(event):
            self.x = event.x
            self.y = event.y
            self.width = self.root.winfo_width()
            self.screen_width = self.root.winfo_screenwidth()

        def perform_resize(event):
            delta_x = event.x - self.x
            new_width = self.width + delta_x
            x_position = self.screen_width - new_width
            self.root.geometry(f"{new_width}x{self.window_height}+{x_position}+0")

        self.top_frame.bind("<Button-1>", start_resize)
        self.top_frame.bind("<B1-Motion>", perform_resize)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
