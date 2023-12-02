import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
from pydub.playback import play
import os

def convert_audio(src, dst):
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    raw_audio = AudioSegment.from_file(dst, format="wav")
    channel_count = raw_audio.channels
    print(f"Channel count before conversion: {channel_count}")
    mono_wav = raw_audio.set_channels(1)
    mono_wav.export("pt_mono.wav", format="wav")
    mono_wav_audio = AudioSegment.from_file("pt_mono.wav", format="wav")
    channel_count = mono_wav_audio.channels
    print(f"Channel count after conversion: {channel_count}")
    return os.path.abspath("pt_mono.wav")

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("Audio files", "*.mp3")])
    if file_path:
        print(f"Selected file: {file_path}")
        converted_file_path = convert_audio(file_path, "pt_mono.wav")

# Create the main window
window = tk.Tk()
window.title("Clap Audio Analysis")

# Set the initial size of the window
window.geometry("300x100")  # width x height

# Create a button to open the file dialog
button = tk.Button(window, text="Open File Dialog", height=2, width=20, command=open_file_dialog)

# Center the button in the window
button.pack(side="top", pady=20)

# Run the Tkinter event loop
window.mainloop()
