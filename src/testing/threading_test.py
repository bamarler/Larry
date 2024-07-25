import threading
import tkinter as tk
from tkinter import messagebox
import ollama

def install_method():
    # Your installation logic here
    print("Installation started...")
    import time
    ollama_pull = ollama.pull("orca-mini:3b", stream=True)  # Simulating a long installation process
    for chunk in ollama_pull:
        status.config(text=f"status: {chunk['status']}")
        try:
            completed.config(text=f"Completed: {chunk['completed']}/{chunk['total']}")
        except KeyError:
            pass
    print("Installation completed.")
    messagebox.showinfo("Install", "Installation completed.")

def start_install():
    install_thread = threading.Thread(target=install_method)
    install_thread.start()

# Setting up the GUI
root = tk.Tk()
root.title("My App")

install_button = tk.Button(root, text="Install", command=start_install)
install_button.pack(pady=20)

status = tk.Label(root)
status.pack()

completed = tk.Label(root)
completed.pack()

root.mainloop()
