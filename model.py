# model.py

from pydub import AudioSegment
import os

class AudioConverter:
    @staticmethod
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
