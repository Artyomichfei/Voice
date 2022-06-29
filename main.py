from email.policy import default
from logging import exception
from re import A
from vosk import Model, KaldiRecognizer
from os import path
from pyaudio import PyAudio, paInt16
import json
from pyowm import OWM
from datetime import datetime
import speak
import os
import signal
import subprocess
import pyautogui

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

counts = {1:"первого",2:"второго",3:"третьего",4:"четвёртого",5:"пятого",6:"шестого",7:"седьмого",8:"восьмого",9:"девятого",10:"десятого",11:"одиннадцатого",12:"двенадцатого",13:"тринадцатого",14:"четырнадцатого",15:"пятнадцатого",16:"шеснадцатого",17:"семнадцатого",18:"восемнадцатого",19:"девятнадцатого",20:"двадцатого",21:"двадцатьпервого",22:"двадцатьвторого",23:"двадцатьтретьего",24:"двадцатьчетвёртого",25:"двадцатьпятого",26:"двадцатьшестого",27:"двадцатьседьмое",28:"двадцатьвосьмого",29:"двадцатьдевятое",30:"тридцатого",31:"тридцатьпервого"}

inz("model-ru")

location = "Aachen,DE"

open_weather_map = OWM(weather_api_key)
open_weather_map.config['language'] = 'ru' # Язык результатов

def status_1():
    now = open_weather_map.weather_manager().weather_at_place(location)
    status = now.weather.detailed_status
    speak.talk(f"Сейчас за окном:{status}")
def temperature_1():
    now = open_weather_map.weather_manager().weather_at_place(location)
    temperature = int(now.weather.temperature('celsius')["temp"])
    speak.talk(f"Температура:{temperature} по цельсию")

def weather(w):
    dates = set()
    for precipitation in w:
         dates.add(datetime.fromisoformat(precipitation.reference_time('iso')).replace(tzinfo=None).day)
    dates = list(dates)
    speech = "Он будет "
    for date in dates:
        speech += counts[date] + " "
        print(counts[date])
    speech += "числа"
    if len(dates):
        speak.talk(speech)
     # print(dates[0:len_1])
def prec():
    forecast = open_weather_map.weather_manager().forecast_at_place(location, '3h')
    if forecast.will_have_rain():
        speak.talk("На неделе будет дождь" )
        weather(forecast.when_rain())
    elif forecast.will_have_snow():
        speak.talk("На неделе будет снег" )
        weather(forecast.when_snow())
    else:
        speak.talk("Осадков не будет на этой неделе")

mus_ind = None
def music_start():
    global mus_ind
    mus_ind = subprocess.Popen("C:/MPC-HC64/mpc-hc64_nvo.exe G:/Музыка") 

def music_stop():
    global mus_ind
    mus_ind.terminate()
    mus_ind = None

def volumeup():
    pyautogui.press("volumeup", presses=3)

def volumedown():
    pyautogui.press("volumedown", presses=3)

def volumemute():
    pyautogui.press("volumemute")

def nexttrack():
    pyautogui.press("nexttrack")

def prevtrack():
    pyautogui.press("prevtrack")

def pause():
    pyautogui.press("Space")

def time():
    if text == "время":
        time_2 = datetime.now()
        result = "Сейчас: "
        result += str(time_2.hour)
        if  time_2.hour == (2,3,4,22,23,24) :
            result += " часа"
            speak.talk(result)
        if 4 > time_2.hour < 21 or time_2.hour == 0:
            result += " часов"
            speak.talk(result)
        if time_2.hour ==(1, 21):
            result += " час"
            speak.talk(result)
        # print(f"Сегодня: {time_2.hour}")

def hello():
    speak.talk("привет")
commands = {"выход": {"func":exit, "param":0 }, 
"привет": {"func":hello, "param":None }, 
"погода": { "func":status_1, "param": None},
"температура":{ "func":temperature_1, "param":None}, 
"осадки":{"func": prec, "param":None}, 
"время": {"func": time, "param": None}, 
"старт":{"func": music_start , "param": None},
"конец":{"func": music_stop, "param":None},
"громче":{"func": volumeup, "param": None},
"тише":{"func":volumedown, "param":None},
"звук":{"func":volumemute, "param": None},
"следующий":{"func":nexttrack, "param":None},
"предыдущий":{"func": prevtrack, "param":None},
"пауза":{"func":pause,"param":None},
} 

speak.init()
speak.talk("Начало работы")
while(True):
    voice = audio_01.read(4000, exception_on_overflow = False)
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


