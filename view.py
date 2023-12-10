import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import os  # Added for os.path.abspath

class AudioConverterView:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Clap Audio Analysis")
        self.window.geometry("800x650")

        self.button = tk.Button(self.window, text="Load File", height=2, width=20, command=self.open_file_dialog)
        self.button.pack(side="top", pady=20)

        # Create a frame to embed the waveform plot
        self.plot_frame = tk.Frame(self.window)
        self.plot_frame.pack(side="top", expand=True, fill="both")

        # Label to display the duration
        self.duration_label = tk.Label(self.window, text="Duration: ")
        self.duration_label.pack(side="top", pady=10)

        # Label to display the resonance
        self.resonance_label = tk.Label(self.window, text="Resonance: ")
        self.resonance_label.pack(side="top", pady=10)

        self.close_button = tk.Button(self.window, text="Done", command=self.window.destroy, fg="red")
        self.close_button.pack(side="bottom", pady=10)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("Audio files", "*.mp3")])
        if file_path:
            print("Selected file:", file_path)
            converted_file_path = self.controller.convert_audio(file_path, "pt_mono.wav")

            # Update the waveform plot and duration label
            self.update_waveform_plot(converted_file_path)
            self.update_duration_label(converted_file_path)
            self.update_highest_resonance(converted_file_path)

    def update_waveform_plot(self, file_path):
        # Read the .wav file
        sample_rate, data = wavfile.read(os.path.abspath(file_path))

        # Calculate the time array
        t = np.arange(0, len(data) / sample_rate, 1 / sample_rate)

        # Ensure the length of t matches the length of data
        if len(t) != len(data):
            t = np.linspace(0, len(data) / sample_rate, len(data))

        # Clear the existing plot (if any)
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

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
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill=tk.BOTH)

    def update_duration_label(self, file_path):
        # Read the .wav file
        sample_rate, data = wavfile.read(os.path.abspath(file_path))

        # Calculate the duration
        duration = len(data) / sample_rate

        # Update the label
        self.duration_label.config(text=f"Duration: {duration:.2f} seconds")

    def update_highest_resonance(self, file_path):
        # Read the audio file
        sample_rate, data = wavfile.read(file_path)

        # Perform FFT on the audio data
        n = len(data) * 10  # Increase the FFT size for better frequency resolution
        fft_result = fft(data, n)
        fft_freqs = fftfreq(n, d=1 / sample_rate)

        # Exclude negative frequencies and find the index of the maximum amplitude
        positive_freqs = fft_freqs[:n // 2]
        magnitude_spectrum = np.abs(fft_result[:n // 2])
        resonance_index = np.argmax(magnitude_spectrum)

        # Calculate the highest resonance frequency
        highest_resonance = positive_freqs[resonance_index]
        # Update the label
        self.resonance_label.config(text=f"Resonance: {highest_resonance:.2f} Hz")

    def run(self):
        self.window.mainloop()
