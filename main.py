from logging import exception
from vosk import Model, KaldiRecognizer
from os import path
from pyaudio import PyAudio, paInt16
import json

der = None
audio_01 = None

def inz(dir):
    global der
    global audio_01
    if not path.exists(dir):
        raise Exception("Директория не найдена")
    # model = Model(dir)
    der = KaldiRecognizer(Model(dir), 16000)

    # PyAudio().open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    audio_01 = PyAudio().open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    audio_01.start_stream()
 
inz("model-ru")

def hello():
    print("привет")
commands = {"выход": {"func":exit, "param":0 }, "привет": {"func":hello, "param":None }}

print("Начало работы")
while(True):
    voice = audio_01.read(4000)
    if len(voice) == 0:
        break
    if der.AcceptWaveform(voice):
        text = json.loads(der.Result())["text"].lower()   
        if len(text) > 0:
            print(text)
            if text in commands:
                command = commands[text] 
                if command["param"] is None:
                    command["func"]()
                else:    
                    command["func"](command["param"])

