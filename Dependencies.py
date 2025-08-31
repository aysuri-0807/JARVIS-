from SETUP import *
import speech_recognition as sr
import os
import pyttsx3


def listen():
    recognizer = sr.Recognizer() #built-in recognizer
    mic = sr.Microphone(device_index=2)
    print("Listening...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source) #Post-Processing
        voice = recognizer.listen(source)

        #Try to recognize
        try:
            text = recognizer.recognize_google(voice)
            return text

        except sr.UnknownValueError:
            return "NAN"

def open_app(app_name):
    os.startfile(paths[app_name])


def readAloud(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()