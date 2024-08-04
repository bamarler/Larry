import tkinter as tk
from tkinter import ttk, font
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

class UISettingsPage(SettingsPage):
    def __init__(self, parent):
        super().__init__(parent, "UI Settings")

        self.settings_manager = SettingsManager()
        self.ui_settings = self.settings_manager.get_ui_settings()

        self.create_font_settings()
        self.create_theme_settings()
        self.create_save_button()

    def create_font_settings(self):
        font_label = tk.Label(self.page, text="Font Settings", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        font_label.pack(pady=10)

        font_frame = tk.Frame(self.page, bg=BACKGROUND_COLOR)
        font_frame.pack(fill=tk.X, padx=10, pady=5)

        font_family_label = tk.Label(font_frame, text="Font:", font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        font_family_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')

        font_families = list(font.families())
        self.font_var = tk.StringVar(value=self.ui_settings['font'])
        font_dropdown = ttk.Combobox(font_frame, textvariable=self.font_var, values=font_families, state='readonly')
        font_dropdown.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

        font_size_label = tk.Label(font_frame, text="Font Size:", font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        font_size_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')

        self.font_size_var = tk.IntVar(value=self.ui_settings['fontsize'])
        font_size_slider = tk.Scale(font_frame, from_=8, to=16, orient=tk.HORIZONTAL, variable=self.font_size_var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, troughcolor=ACCENT_COLOR, bd=0, highlightthickness=0)
        font_size_slider.grid(row=1, column=1, padx=5, pady=2, sticky='ew')

        font_frame.grid_columnconfigure(1, weight=1)

    def create_theme_settings(self):
        theme_label = tk.Label(self.page, text="Theme Settings", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        theme_label.pack(pady=10)

        theme_frame = tk.Frame(self.page, bg=BACKGROUND_COLOR)
        theme_frame.pack(fill=tk.X, padx=10, pady=5)

        self.theme_var = tk.StringVar(value=self.ui_settings['theme'])
        themes = self.ui_settings['themes']
        
        for theme_name, colors in themes.items():
            theme_inner_frame = tk.Frame(theme_frame, bg=BACKGROUND_COLOR)
            theme_inner_frame.pack(fill=tk.X, padx=5, pady=2, anchor='w')
            
            color_frame = tk.Frame(theme_inner_frame, bg=BACKGROUND_COLOR)
            color_frame.pack(side=tk.RIGHT, padx=10, pady=2)

            for color_key, color_value in colors.items():
                color_box = tk.Frame(color_frame, bg=color_value, width=20, height=20)
                color_box.pack(side=tk.LEFT, padx=2)
            
            theme_radio = tk.Radiobutton(theme_inner_frame, text=theme_name, variable=self.theme_var, value=theme_name, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=ACCENT_COLOR, bd=0, indicatoron=0)
            theme_radio.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def create_save_button(self):
        save_button = tk.Button(self.page, text="Save", command=self.save_settings, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        save_button.pack(pady=20)

    def save_settings(self):
        new_settings = {
            "font": self.font_var.get(),
            "fontsize": self.font_size_var.get(),
            "theme": self.theme_var.get(),
            "themes": self.ui_settings["themes"]  # Assuming themes are not changed by the user
        }
        self.settings_manager.set_ui_settings(new_settings)
        # Update the UI constants
        ui_constants.FONT = new_settings["font"]
        ui_constants.FONTSIZE = new_settings["fontsize"]
        selected_theme = new_settings["themes"][new_settings["theme"]]
        ui_constants.BACKGROUND_COLOR = selected_theme["background_color"]
        ui_constants.HEADER_COLOR = selected_theme["header_color"]
        ui_constants.ACCENT_COLOR = selected_theme["accent_color"]
        ui_constants.TEXT_COLOR = selected_theme["text_color"]

        ui_constants.init_ui()



# Usage example for standalone testing
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    page = UISettingsPage(root)
    page.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
