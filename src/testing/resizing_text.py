import tkinter as tk

class AutoScalingText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg='#2C2F33', fg='#d3d3d3', **kwargs)
        self.bind('<KeyRelease>', self._resize)

    def _resize(self, event=None):
        # Calculate the number of lines and columns in the text widget
        lines = int(self.index('end-1c').split('.')[0])
        max_length = max(len(line) for line in self.get('1.0', 'end-1c').split('\n'))
        
        # Set the height and width of the text widget
        self.config(height=lines, width=max_length)

def main():
    root = tk.Tk()
    root.title("Auto Scaling Text Widget")

    # Create an instance of AutoScalingText with initial size 1x1
    auto_text = AutoScalingText(root, height=1, width=1)
    auto_text.pack()

    # Insert some initial text
    auto_text.insert('1.0', "Type here...")

    root.mainloop()

if __name__ == "__main__":
    main()
