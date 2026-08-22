import os
from os import path
from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar = False)

def speak(text, output_path="output.wav"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path

def play_audio(file_path):
    if os.name == "nt":
        os.startfile(file_path)
    else:
        os.system(f"afplay {file_path}" if os.name == "darwin" else f"aplay {file_path}")
