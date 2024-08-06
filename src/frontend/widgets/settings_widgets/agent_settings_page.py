import tkinter as tk
from tkinter import ttk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

from src.frontend.ui_constants import ui_constants
from src.frontend.widgets.settings_widgets.settings_page import SettingsPage
from src.backend.settings_manager import SettingsManager

FONT = ui_constants.FONT
FONTSIZE = ui_constants.FONTSIZE
BACKGROUND_COLOR = ui_constants.BACKGROUND_COLOR
HEADER_COLOR = ui_constants.HEADER_COLOR
ACCENT_COLOR = ui_constants.ACCENT_COLOR
TEXT_COLOR = ui_constants.TEXT_COLOR

class AgentSettingsPage(SettingsPage):
    def __init__(self, parent):
        super().__init__(parent, "Agent Settings")

        self.settings_manager = SettingsManager()
        self.agent_settings = self.settings_manager.get_agent_settings()

        self.default_agent_settings = self.settings_manager.default_agent_settings

        self.create_scrollable_canvas()

    def create_scrollable_canvas(self):
        # Create a canvas with a scrollbar
        self.canvas = tk.Canvas(self.page, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack_propagate(False)  # Prevent the canvas from resizing due to its content
        self.scrollbar = tk.Scrollbar(self.page, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=5)

        # Bind mouse wheel to scroll
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)

        self.create_settings_page(self.scrollable_frame)
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def create_settings_page(self, frame):
        header = tk.Label(frame, text="Agent Settings", font=(FONT, FONTSIZE + 4, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        header.pack(pady=10)

        # Dropdown and buttons
        top_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        top_frame.pack(fill='x', pady=5)

        agent_label = tk.Label(top_frame, text="Select Agent:", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        agent_label.pack(side="left", padx=5)

        self.agent_var = tk.StringVar(value="classic larry")
        agent_list = [agent for agent in self.agent_settings["agents"].keys() if agent != self.agent_var.get()]
        self.agent_dropdown = ttk.Combobox(top_frame, textvariable=self.agent_var, values=agent_list, font=(FONT, FONTSIZE), state="readonly")
        self.agent_dropdown.pack(side="left", padx=5)

        remove_button = tk.Button(top_frame, text="Remove Agent", font=(FONT, FONTSIZE), bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0, command=self.remove_agent)
        remove_button.pack(side="left", padx=5)

        create_button = tk.Button(top_frame, text="Create New Agent", font=(FONT, FONTSIZE), bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0, command=self.create_agent)
        create_button.pack(side="left", padx=5)

        save_button = tk.Button(top_frame, text="Save Agent", font=(FONT, FONTSIZE), bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0, command=self.save_agent)
        save_button.pack(side="left", padx=5)

        # Agent details
        self.agent_details_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        self.agent_details_frame.pack(fill='both', expand=True, pady=10)

        self.create_agent_details(self.agent_var.get())

        # Update details when a new agent is selected
        self.agent_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_agent_details())

    def create_agent_details(self, agent_name):
        self.clear_frame(self.agent_details_frame)
        agent = self.agent_settings["agents"].get(agent_name, {})

        details_frame = tk.Frame(self.agent_details_frame, bg=BACKGROUND_COLOR)
        details_frame.pack(fill='x', pady=5)

        fields = [
            ("Agent Label:", agent_name),
            ("Name:", agent.get("name", "")),
            ("Role:", agent.get("role", "")),
            ("Personality (adjectives):", agent.get("personality", ""))
        ]

        self.agent_entries = []
        for i, (label_text, value) in enumerate(fields):
            label = tk.Label(details_frame, text=label_text, font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')

            entry = tk.Entry(details_frame, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            
            self.agent_entries.append(entry)

        details_frame.columnconfigure(1, weight=1)

        behaviors_label = tk.Label(self.agent_details_frame, text="Behaviors", font=(FONT, FONTSIZE + 2, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        behaviors_label.pack(pady=10)

        behaviors = agent.get("behaviors", [])

        self.behavior_entries = {}
        for i, behavior in enumerate(behaviors):
            self.create_behavior_entry(i, behavior)

        # Create New Behavior button
        self.add_behavior_button = tk.Button(self.agent_details_frame, text="Create New Behavior", font=(FONT, FONTSIZE), bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0, command=self.add_behavior)
        self.add_behavior_button.pack(pady=10)

    def create_behavior_entry(self, index, behavior):
        frame = tk.Frame(self.agent_details_frame, bg=BACKGROUND_COLOR)
        frame.pack(fill='x', pady=5)

        label = tk.Label(frame, text=f"Behavior {index + 1}:", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        label.pack(side="left", padx=5, anchor="n")  # Align to the top (north)

        entry = tk.Text(frame, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, height=5, wrap='word', width=50)
        entry.insert("1.0", behavior)
        entry.pack(side="left", fill='x', expand=True, padx=5)

        remove_button = tk.Button(frame, text="Remove Behavior", font=(FONT, FONTSIZE), bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0, command=lambda idx=index: self.remove_behavior(idx, frame))
        remove_button.pack(side="left", padx=5, anchor="n")  # Align to the top (north)

        self.behavior_entries[index] = entry

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def update_agent_details(self):
        self.create_agent_details(self.agent_var.get())
        self.update_agent_dropdown_values()

    def remove_agent(self):
        agent_name = self.agent_var.get()
        if agent_name in self.agent_settings["agents"]:
            del self.agent_settings["agents"][agent_name]
            self.settings_manager.set_agent_settings(self.agent_settings)
            self.update_agent_dropdown_values()

    def create_agent(self):
        new_agent_name = "New Agent"
        self.agent_settings["agents"][new_agent_name] = {
            "name": "",
            "role": "",
            "personality": "",
            "behaviors": {}
        }
        self.settings_manager.set_agent_settings(self.agent_settings)
        self.update_agent_dropdown_values()
        self.agent_var.set(new_agent_name)
        self.update_agent_details()

    def save_agent(self):
        agent_name = self.agent_var.get()
        if agent_name in self.agent_settings["agents"]:
            agent = self.agent_settings["agents"][agent_name]

            # Fetch entries from agent_details_frame
            entries = self.agent_entries
            
            print(entries)
            for i, entry in enumerate(entries):
                text = entry.get()
                print(f"{text}\n")
                if i == 0:
                    new_agent_name = text
                    self.agent_settings["agents"][new_agent_name] = self.agent_settings["agents"].pop(agent_name)
                    agent_name = new_agent_name
                    self.agent_var.set(new_agent_name)
                elif i == 1:
                    agent["name"] = text
                elif i == 2:
                    agent["role"] = text
                elif i == 3:
                    agent["personality"] = text

            agent["behaviors"] = [entry.get("1.0", "end-1c") for entry in self.behavior_entries.values()]

            self.settings_manager.set_agent_settings(self.agent_settings)
            self.update_agent_dropdown_values()

    def add_behavior(self):
        index = len(self.behavior_entries)
        self.create_behavior_entry(index, "")
        # Re-pack the "Create New Behavior" button to ensure it's at the bottom
        self.add_behavior_button.pack_forget()
        self.add_behavior_button.pack(pady=10)

    def remove_behavior(self, index, frame):
        print(f"Index: {index} Length: {len(self.behavior_entries)}")
        if index in self.behavior_entries:
            frame.pack_forget()
            del self.behavior_entries[index]
            # Reindex remaining behaviors
            self.behavior_entries = {i if i < index else i - 1: entry for i, entry in self.behavior_entries.items()}
            self.update_behavior_labels()

    def update_behavior_labels(self):
        for i, entry in sorted(self.behavior_entries.items()):
            entry.master.children['!label'].config(text=f"Behavior {i + 1}:")
            remove_button = entry.master.children['!button']
            remove_button.config(command=lambda idx=i: self.remove_behavior(idx, entry.master))

    def update_agent_dropdown_values(self):
        agent_list = [agent for agent in self.agent_settings["agents"].keys() if agent != self.agent_var.get()]
        self.agent_dropdown['values'] = agent_list

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    page = AgentSettingsPage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()

