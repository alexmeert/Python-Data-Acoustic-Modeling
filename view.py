# view.py will deal with all things visual like the tkinter GUI
import tkinter as tk
from tkinter import filedialog

class AudioConverterView:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Clap Audio Analysis")
        self.window.geometry("300x100")

        self.button = tk.Button(self.window, text="Open File Dialog", height=2, width=20, command=self.controller.open_file_dialog)
        self.button.pack(side="top", pady=20)

    def run(self):
        self.window.mainloop()
