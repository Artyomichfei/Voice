from logging import exception
from vosk import Model, KaldiRecognizer
from os import path
from pyaudio import PyAudio, paInt16
import json
from pyowm import OWM
from datetime import datetime

der = None
audio_01 = None

with open("api_key", "r") as file:
    weather_api_key = file.read()
print("Используется такой ключ:", weather_api_key)

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

location = "Aachen,DE"

open_weather_map = OWM(weather_api_key)
open_weather_map.config['language'] = 'ru' # Язык результатов

 # запрос данных о текущем состоянии погоды
now = open_weather_map.weather_manager().weather_at_place(location)
forecast = open_weather_map.weather_manager().forecast_at_place(location, '3h') # 3h вернет недельный, так как daily не работает 

status = now.weather.detailed_status
temperature = int(now.weather.temperature('celsius')["temp"])
def status_1(status):
    print("Сейчас за окном:", status)
def temperature_1(temperature):
    print("Температура:", temperature)

def weather(w):
    dates = set()
    for precipitation in w:
         dates.add(precipitation.reference_time('iso').split()[0])
    for date in dates:
        print(date)
def prec():
    if forecast.will_have_rain():
        print("На неделе будет дождь" )
        weather(forecast.when_rain())
    elif forecast.will_have_snow():
        print("На неделе будет снег" )
        weather(forecast.when_snow())
    else:
        print("Осадков не будет на этой неделе")

def time():
    print(datetime.now())

def hello():
    print("привет")
commands = {"выход": {"func":exit, "param":0 }, "привет": {"func":hello, "param":None }, "погода": { "func":status_1, "param": status}, "температура":{ "func":temperature_1, "param":temperature}, "осадки":{"func": prec, "param":None}, "время": {"func": time, "param": None}}

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

