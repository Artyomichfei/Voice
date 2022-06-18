import pyttsx3 

tts = None
def init():
    global tts
    tts = pyttsx3.init()
    rate = tts.getProperty('rate')
    tts.setProperty('rate', rate-40)
    volume = tts.getProperty('volume')
    tts.setProperty('volume', volume+0.9)
    voices = tts.getProperty('voices')
    for voi in voices:
        # print(voi.name)
        if "Russian" in voi.name:
            tts.setProperty('voice', voi.id)
            break

def talk(text):
    tts.say(text)
    tts.runAndWait()



