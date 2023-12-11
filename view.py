import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from scipy.io import wavfile
from scipy.signal import welch
import os
import matplotlib.pyplot as plt

class AudioConverterView:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Clap Audio Analysis")
        self.window.maxsize(820, 670)

        # Set background colors
        bg_color = "#F0F0F0"  # Light gray

        # File selection section
        self.file_frame = tk.Frame(self.window, pady=20, bg=bg_color)
        self.file_frame.grid(row=0, column=0, columnspan=3)

        self.button = tk.Button(self.file_frame, text="Load File", height=2, width=20, command=self.open_file_dialog)
        self.button.grid(row=0, column=0, padx=10)

        # Selected File Label
        self.filename_label = tk.Label(self.file_frame, text="Selected File: ", bg=bg_color)
        self.filename_label.grid(row=0, column=1, padx=10)

        # Plot section
        self.plot_frame = tk.Frame(self.window, bg=bg_color)
        self.plot_frame.grid(row=1, column=0, columnspan=5, pady=10, padx=10, sticky="nsew")

        # Duration label
        self.duration_label = tk.Label(self.window, text="Duration: ", bg=bg_color)
        self.duration_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        # Resonance label
        self.resonance_label = tk.Label(self.window, text="Resonance: ", bg=bg_color)
        self.resonance_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        # Control buttons section
        self.button_frame = tk.Frame(self.window, bg=bg_color)
        self.button_frame.grid(row=5, column=0, columnspan=5, pady=10, padx=10, sticky="w")

        self.close_button = tk.Button(self.button_frame, text="Close", command=self.window.destroy, fg="red")
        self.close_button.grid(row=0, column=0, padx=10)

        # Combine plots button
        self.merge_button = tk.Button(self.button_frame, text="Combine Frequency Plots", command=self.combine_plots)
        self.merge_button.grid(row=0, column=1, padx=10)


        # Buttons to select which plot is shown
        var = tk.IntVar()
        self.lowButton = tk.Radiobutton(text="Low", variable=var, value=1, command=self.update_lowFreq_plot)
        self.midButton = tk.Radiobutton(text="Mid", variable=var, value=2, command=self.update_midFreq_plot)
        self.highButton = tk.Radiobutton(text="High", variable=var, value=3, command=self.update_highFreq_plot)
        self.waveformButton = tk.Radiobutton(text="Waveform", variable=var, value=4, command=self.update_waveform_plot)
        self.lowButton.grid(row=2, column=1, padx=5)
        self.midButton.grid(row=2, column=2, padx=5)
        self.highButton.grid(row=2, column=3, padx=5)
        self.waveformButton.grid(row=2, column=4, padx=5)

        # Variable to store loaded file path and converted file path
        self.loaded_file_path = None
        self.converted_file_path = None

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("Audio files", "*.mp3")])
        filename = os.path.basename(file_path)
        if file_path:
            print("Selected file:", file_path)
            self.loaded_file_path = file_path
            self.converted_file_path = self.controller.convert_audio(file_path, "pt_mono.wav")

            # Update the waveform plot and duration label
            self.update_waveform_plot()
            self.update_duration_label()
            self.update_highest_resonance()
            self.update_selected_file(filename)

    def update_selected_file(self, filename):
        self.filename_label.config(text=f"Selected File: {filename}")

    def update_waveform_plot(self):
        if self.converted_file_path:
            # Read the .wav file
            sample_rate, data = wavfile.read(os.path.abspath(self.converted_file_path))

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
            ax.plot(t, data, color='blue')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude (dB)')
            ax.set_title('Waveform of Audio')
            ax.grid()

            # Create the canvas to display the plot
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(expand=True, fill=tk.BOTH)

            print("Updated waveform plot")

        else:
            print("No audio file loaded. Please load an audio file first.")

    def combine_plots(self):
        if self.loaded_file_path:
            converted_file_path = self.controller.convert_audio(self.loaded_file_path, "pt_mono.wav")

            # Get the frequencies and power for each frequency band
            low_frequencies, low_power = self.get_frequency_band(converted_file_path, "low")
            mid_frequencies, mid_power = self.get_frequency_band(converted_file_path, "mid")
            high_frequencies, high_power = self.get_frequency_band(converted_file_path, "high")

            # Plot the combined frequency plots
            fig, ax = plt.subplots(figsize=(8, 4))

            # Plot low frequencies
            ax.plot(low_frequencies, low_power, label='Low Frequencies', color='purple')

            # Plot mid frequencies
            ax.plot(mid_frequencies, mid_power, label='Mid Frequencies', color='green')

            # Plot high frequencies
            ax.plot(high_frequencies, high_power, label='High Frequencies', color='red')

            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Power/Frequency (dB/Hz)')
            ax.set_title('Combined Frequency Plots')
            ax.legend()
            ax.grid(True)

            # Clear the existing plot (if any)
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            # Create the canvas to display the plot
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(expand=True, fill=tk.BOTH)

            print("Combined frequency plots")

        else:
            print("No audio file loaded. Please load an audio file first.")

    def get_frequency_band(self, file_path, band):
        sample_rate, data = wavfile.read(file_path)

        # Perform FFT
        n = len(data)
        fft_result = np.fft.fft(data)
        frequencies = np.fft.fftfreq(n, d=1 / sample_rate)

        # Define frequency bands
        low_cutoff = 20
        mid_cutoff = 2000
        high_cutoff = 20000

        # Index of frequency bands
        low_indices = np.where((frequencies >= 0) & (frequencies < low_cutoff))
        mid_indices = np.where((frequencies >= low_cutoff) & (frequencies < mid_cutoff))
        high_indices = np.where((frequencies >= mid_cutoff) & (frequencies < high_cutoff))

        if band == "low":
            return frequencies[low_indices], np.abs(fft_result[low_indices])
        elif band == "mid":
            return frequencies[mid_indices], np.abs(fft_result[mid_indices])
        elif band == "high":
            return frequencies[high_indices], np.abs(fft_result[high_indices])

    def update_lowFreq_plot(self):
        self.plot_frequency_band("low")

    def update_midFreq_plot(self):
        self.plot_frequency_band("mid")

    def update_highFreq_plot(self):
        self.plot_frequency_band("high")

    def plot_frequency_band(self, band):
        if self.loaded_file_path:
            file_path = "pt_mono.wav"
            sample_rate, data = wavfile.read(file_path)

            # Perform FFT
            n = len(data)
            fft_result = np.fft.fft(data)
            frequencies = np.fft.fftfreq(n, d=1/sample_rate)

            # Define frequency bands
            low_cutoff = 20
            mid_cutoff = 2000
            high_cutoff = 20000

            # Index of frequency bands
            low_indices = np.where((frequencies >= 0) & (frequencies < low_cutoff))
            mid_indices = np.where((frequencies >= low_cutoff) & (frequencies < mid_cutoff))
            high_indices = np.where((frequencies >= mid_cutoff) & (frequencies < high_cutoff))

            # Plot selected frequency band
            fig = Figure(figsize=(8, 4))
            ax = fig.add_subplot(111)

            if band == "low":
                ax.plot(frequencies[low_indices], np.abs(fft_result[low_indices]), color='purple', label='Low Frequencies')
            elif band == "mid":
                ax.plot(frequencies[mid_indices], np.abs(fft_result[mid_indices]), color='green', label='Mid Frequencies')
            elif band == "high":
                ax.plot(frequencies[high_indices], np.abs(fft_result[high_indices]), color='red', label='High Frequencies')

            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Amplitude')
            ax.set_title(f'{band.capitalize()} Frequency Band')
            ax.legend()
            ax.grid()

            # Clear the existing plot (if any)
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            # Create the canvas to display the plot
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(expand=True, fill=tk.BOTH)

            print(f"Updated {band} frequency plot")

        else:
            print("No audio file loaded. Please load an audio file first.")

    def update_duration_label(self):
        if self.converted_file_path:
            # Read the .wav file
            sample_rate, data = wavfile.read(os.path.abspath(self.converted_file_path))

            # Calculate the duration
            duration = len(data) / sample_rate

            # Update the label
            self.duration_label.config(text=f"Duration: {duration:.2f} seconds")

    def update_highest_resonance(self):
        if self.converted_file_path:
            # Read the audio file
            sample_rate, data = wavfile.read(self.converted_file_path)

            frequencies, power = welch(data, sample_rate, nperseg=4096)
            dominant_frequency = frequencies[np.argmax(power)]

            # Update the label
            self.resonance_label.config(text=f"Resonance: {dominant_frequency:.2f} Hz")

    def run(self):
        self.window.mainloop()
