import os
from os import path
from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar = False)

def speak(text, out_path="output_audio/answer.wav"):
    if not text or not text.strip():
        print("[TTS] Skipped speaking — empty or blank text.")
        return None

    dir_name = os.path.dirname(out_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    try:
        tts.tts_to_file(text=text, file_path=out_path)
    except Exception as e:
        print(f"[TTS] Failed to generate audio: {e}")
        return None

    return os.path.abspath(out_path)


def play_audio(file_path):
    if os.name == "nt":
        os.startfile(file_path)
    else:
        os.system(f"afplay {file_path}" if os.uname().sysname == "darwin" else f"xdg-open '{file_path}'")
