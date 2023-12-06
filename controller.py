from model import AudioConverter
from view import AudioConverterView
from tkinter import filedialog

class AudioConverterController:
    def __init__(self):
        self.model = AudioConverter()
        self.view = AudioConverterView(self)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("Audio files", "*.mp3")])
        if file_path:
            print(f"Selected file: {file_path}")
            converted_file_path, duration_seconds = self.model.convert_audio(file_path, "pt_mono.wav")
            self.view.update_duration_label(duration_seconds)

if __name__ == "__main__":
    controller = AudioConverterController()
    controller.view.run()
