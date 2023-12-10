import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from scipy.io import wavfile
import os  # Added for os.path.abspath

class AudioConverterView:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Clap Audio Analysis")
        self.window.geometry("300x150")

        self.button = tk.Button(self.window, text="Open File Dialog", height=2, width=20, command=self.open_file_dialog)
        self.button.pack(side="top", pady=20)

        self.close_button = tk.Button(self.window, text="Exit", command=self.window.destroy, fg="red")
        self.close_button.pack(side="bottom", pady=10)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("Audio files", "*.mp3")])
        if file_path:
            print("Selected file:", file_path)
            converted_file_path = self.controller.convert_audio(file_path, "pt_mono.wav")

            # Open the waveform plot popup
            self.show_waveform_popup(converted_file_path)

    def show_waveform_popup(self, file_path):
        popup = tk.Toplevel(self.window)
        popup.title("Waveform Plot")

        # Read the .wav file
        sample_rate, data = wavfile.read(os.path.abspath(file_path))

        # Calculate the time array
        t = np.arange(0, len(data) / sample_rate, 1 / sample_rate)

        # Ensure the length of t matches the length of data
        if len(t) != len(data):
            t = np.linspace(0, len(data) / sample_rate, len(data))

        # Create a Figure and set of Axes
        fig = Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)

        # Plot the waveform
        ax.plot(t, data, color='#004bc6')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude (dB)')
        ax.set_title('Waveform of Audio')
        ax.grid()

        # Create the canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.window.mainloop()
