import tkinter as tk
from tkinter import filedialog
import os
import librosa
from os import path 
from pydub import AudioSegment 

class AudioFileLoaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Audio File Loader')
        self.geometry('400x150')

        self.init_ui()

    def init_ui(self):
        self.load_button = tk.Button(self, text='Load Audio File', command=self.load_audio_file)
        self.load_button.place(x=20, y=20, width=150, height=40)

        self.file_label = tk.Label(self, text='No file loaded')
        self.file_label.place(x=20, y=80, width=360, height=40)

    def load_audio_file(self):
        file_name = filedialog.askopenfilename(title='Open Audio File', filetypes=[('Audio Files', '*.wav;*.mp3;*.ogg'), ('All Files', '*.*')])
        if file_name:
            file_name_only = os.path.basename(file_name)  # Extract the file name without the directory
            self.file_label.config(text=f'Loaded File: {file_name_only}')

            if not file_name_only.endswith('.wav'):
                converted_file_name = os.path.splitext(file_name_only)[0] + '.wav'
                audio, sr = librosa.load(file_name, sr=None)
                librosa.output.write_wav(converted_file_name, audio, sr)
                self.file_label.config(text=f'Loaded File (Converted to .wav): {converted_file_name}')

if __name__ == '__main__':
    app = AudioFileLoaderApp()
    app.mainloop()

# files
src = "transcript.mp3"
dst = "test.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
