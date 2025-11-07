# jarvis_basic.py
# Author: Siddharth Ravada
# Version: 0.1 – Basic Voice Assistant

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)   # [0] male, [1] female – you can change this
engine.setProperty('rate', 175)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        listener.pause_threshold = 1
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        if 'jarvis' in command:
            command = command.replace('jarvis', '').strip()
    except:
        return ""
    return command

def run_jarvis():
    talk("Hello sir, I am online. How can I help you?")
    while True:
        command = listen()
        if command == "":
            continue
        print("You said:", command)

        # Logic
        if 'play' in command:
            song = command.replace('play', '').strip()
            talk('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + time)

        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            info = wikipedia.summary(person, 1)
            talk(info)

        elif 'joke' in command:
            joke = pyjokes.get_joke()
            talk(joke)

        elif 'remember' in command:
            data = command.replace('remember', '').strip()
            with open('jarvis_memory.txt', 'a') as f:
                f.write(data + '\n')
            talk("I will remember that, sir.")

        elif 'what did you remember' in command:
            if os.path.exists('jarvis_memory.txt'):
                with open('jarvis_memory.txt', 'r') as f:
                    memories = f.read()
                if memories:
                    talk("You asked me to remember the following:")
                    talk(memories)
                else:
                    talk("I have nothing stored yet, sir.")
            else:
                talk("I don't have any saved memories yet, sir.")

        elif 'stop' in command or 'sleep' in command:
            talk("Going offline. Goodbye, sir.")
            break

        else:
            talk("Sorry sir, I didn’t catch that. Please repeat.")

# Start JARVIS
if __name__ == "__main__":
    talk("Initializing systems...")
    run_jarvis()
