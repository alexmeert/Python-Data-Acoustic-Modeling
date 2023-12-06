# view.py
import tkinter as tk
from tkinter import filedialog

class AudioConverterView:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Clap Audio Analysis")
        self.window.geometry("300x200")

        self.button = tk.Button(self.window, text="Open File Dialog", height=2, width=20, command=self.controller.open_file_dialog)
        self.button.pack(side="top", pady=20)

        self.duration_label = tk.Label(self.window, text="Duration: N/A")
        self.duration_label.pack(side="top", pady=10)

        self.close_button = tk.Button(self.window, text="Done", command=self.window.destroy, fg="red")
        self.close_button.pack(side="bottom", pady=10)

    def update_duration_label(self, duration):
        self.duration_label.config(text=f"Duration: {duration} seconds")

    def run(self):
        self.window.mainloop()

class AudioConverterController:
    def __init__(self):
        self.view = AudioConverterView(self)

    def open_file_dialog(self):
        file_path, duration_seconds = self.controller.convert_audio("input.mp3", "output.wav")  # Replace with actual paths
        print("Selected file:", file_path)
        self.view.update_duration_label(duration_seconds)
        self.view.run()

    def convert_audio(self, src, dst):
        return self.model.convert_audio(src, dst)

if __name__ == "__main__":
    controller = AudioConverterController()
    controller.view.run()
