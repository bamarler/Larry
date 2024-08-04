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

class ModelSettingsPage(SettingsPage):
    def __init__(self, parent):
        super().__init__(parent, "Model Options")

        self.settings_manager = SettingsManager()
        self.model_settings = self.settings_manager.get_model_settings()

        self.default_model_settings = self.settings_manager.default_model_settings

        self.create_scrollable_canvas()

    def create_scrollable_canvas(self):
        # Create a canvas with a scrollbar
        self.canvas = tk.Canvas(self.page, bg=BACKGROUND_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.page, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel to scroll
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)

        self.create_settings_page(scrollable_frame)

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 5:
                self.canvas.yview_scroll(1, "units")
            elif event.num == 4:
                self.canvas.yview_scroll(-1, "units")

    def create_settings_page(self, parent_frame):
        model_label = tk.Label(parent_frame, text="Model Settings", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        model_label.grid(row=0, column=0, columnspan=3, pady=(10, 5), sticky='n')

        self.create_slider(parent_frame, 1, "Temperature", "temperature", 0.1, 2.0, 0.1, "Controls the randomness of the predictions. Lower values make the output more deterministic.")
        self.create_slider(parent_frame, 3, "Top K", "top_k", 1, 100, 1, "The number of highest probability vocabulary tokens to keep for top-k-filtering.")
        self.create_slider(parent_frame, 5, "Top P", "top_p", 0.0, 1.0, 0.01, "If set to < 1.0, only the tokens with top cumulative probability are kept for generation.")
        self.create_slider(parent_frame, 7, "Num Predict", "num_predict", 4000, 16000, 250, "The number of tokens to predict.")
        self.create_slider(parent_frame, 9, "Frequency Penalty", "frequency_penalty", 0.0, 2.0, 0.1, "Penalty for repeated tokens in the text.")
        self.create_slider(parent_frame, 11, "Presence Penalty", "presence_penalty", 0.0, 2.0, 0.1, "Penalty for repeated tokens in the text based on their presence.")
        self.create_slider(parent_frame, 13, "Repeat Penalty", "repeat_penalty", 0.8, 2.0, 0.1, "Penalty for repeated sequences of tokens.")
        self.create_slider(parent_frame, 15, "Repeat Last N", "repeat_last_n", 1, 100, 1, "Number of last tokens to penalize for repetition.")
        self.create_slider(parent_frame, 17, "Mirostat", "mirostat", 0, 2, 1, "Controls the dynamic adjustment of the sampling process.")
        self.create_slider(parent_frame, 19, "Mirostat Tau", "mirostat_tau", 0.1, 10.0, 0.1, "Target perplexity for Mirostat.")
        self.create_slider(parent_frame, 21, "Mirostat Eta", "mirostat_eta", 0.001, 1.0, 0.001, "Learning rate for Mirostat.")
        self.create_slider(parent_frame, 23, "Num Thread", "num_thread", 1, 16, 1, "Number of threads to use.")
        self.create_slider(parent_frame, 25, "Num Ctx", "num_ctx", 128, 2048, 128, "Context window size.")

        self.create_save_button(parent_frame)

    def create_slider(self, parent_frame, row, label_text, setting_key, min_value, max_value, resolution, tooltip_text):
        label = tk.Label(parent_frame, text=f"{label_text}:", font=(FONT, FONTSIZE, 'bold'), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor='w')
        label.grid(row=row, column=0, padx=5, pady=(10, 2), sticky='w')

        tooltip_label = tk.Label(parent_frame, text=tooltip_text, font=(FONT, FONTSIZE - 2), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, wraplength=450, justify='left')
        tooltip_label.grid(row=row, column=1, columnspan=2, padx=5, pady=(10, 2), sticky='w')

        if setting_key not in self.model_settings:
            raise KeyError(f"'{setting_key}' not found in model_settings: {self.model_settings}")

        value = tk.DoubleVar(value=self.model_settings[setting_key])
        slider = tk.Scale(parent_frame, from_=min_value, to=max_value, orient=tk.HORIZONTAL, variable=value, resolution=resolution, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, troughcolor=ACCENT_COLOR, highlightbackground=ACCENT_COLOR, bd=0, highlightthickness=0)
        slider.grid(row=row + 1, column=0, columnspan=3, padx=5, pady=(2, 20), sticky='ew')

        setattr(self, f"{setting_key}_var", value)

        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_columnconfigure(0, weight=0)
    
    # Add the new method to reset to default settings
    def reset_to_default(self):
        self.model_settings = self.default_model_settings
        
        for setting_key, default_value in self.default_model_settings.items():
            slider_var = getattr(self, f"{setting_key}_var", None)
            if slider_var:
                slider_var.set(default_value)

    def create_save_button(self, parent_frame):
        save_button = tk.Button(parent_frame, text="Save", command=self.save_settings, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        save_button.grid(row=27, columnspan=3, pady=20)

        reset_button = tk.Button(parent_frame, text="Reset to Default", command=self.reset_to_default, font=(FONT, FONTSIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0)
        reset_button.grid(row=27, column=2, pady=20, padx=(10, 0))

    def save_settings(self):
        new_settings = {
            "temperature": self.temperature_var.get(),
            "top_k": self.top_k_var.get(),
            "top_p": self.top_p_var.get(),
            "num_predict": self.num_predict_var.get(),
            "frequency_penalty": self.frequency_penalty_var.get(),
            "presence_penalty": self.presence_penalty_var.get(),
            "repeat_penalty": self.repeat_penalty_var.get(),
            "repeat_last_n": self.repeat_last_n_var.get(),
            "mirostat": self.mirostat_var.get(),
            "mirostat_tau": self.mirostat_tau_var.get(),
            "mirostat_eta": self.mirostat_eta_var.get(),
            "num_thread": self.num_thread_var.get(),
            "num_ctx": self.num_ctx_var.get(),
        }
        self.settings_manager.set_model_settings(new_settings)

# Usage example for standalone testing
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x800")
    page = ModelSettingsPage(root)
    page.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
