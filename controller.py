from model import AudioConverter
from view import AudioConverterView

class AudioConverterController:
    def __init__(self):
        self.model = AudioConverter()
        self.view = AudioConverterView(self)

    def convert_audio(self, src, dst):
        return self.model.convert_audio(src, dst)

    def open_file_dialog(self):
        self.view.open_file_dialog()

    def run(self):
        self.view.run()

if __name__ == "__main__":
    controller = AudioConverterController()
    controller.run()
