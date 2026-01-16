import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import subprocess
import spacy
import requests
from datetime import datetime

# ================= INITIALIZATION =================

nlp = spacy.load("en_core_web_sm")

engine = pyttsx3.init()
engine.setProperty("rate", 175)

recognizer = sr.Recognizer()
mic = sr.Microphone()

WAKE_WORD = "jarvis"
conversation_memory = []

# ================= SPEAK =================

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ================= LISTEN =================

def listen():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return ""

# ================= NLP INTENT =================

def get_intent(text):
    doc = nlp(text)

    if "open" in text:
        return "OPEN_APP"
    if "time" in text:
        return "TIME"
    if "date" in text:
        return "DATE"
    if "exit" in text or "shutdown" in text:
        return "EXIT"
    return "LLM"

# ================= ACTION HANDLER =================

def handle_action(intent, text):
    if intent == "TIME":
        speak(datetime.now().strftime("The time is %I:%M %p"))

    elif intent == "DATE":
        speak(datetime.now().strftime("Today is %B %d, %Y"))

    elif intent == "OPEN_APP":
        if "chrome" in text:
            subprocess.Popen("chrome")
            speak("Opening Chrome")
        elif "youtube" in text:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        else:
            speak("I don't recognize that application")

    elif intent == "EXIT":
        speak("Shutting down. Goodbye.")
        exit()

    else:
        response = ask_llm(text)
        speak(response)

# ================= LLM BRAIN =================
# OPTION 1: OPENAI (Cloud)
# OPTION 2: LOCAL LLM (Ollama)

USE_OLLAMA = True

def ask_llm(prompt):
    conversation_memory.append({"role": "user", "content": prompt})

    if USE_OLLAMA:
        return ask_ollama(prompt)
    else:
        return ask_openai(prompt)

def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

def ask_openai(prompt):
    import openai
    openai.api_key = "YOUR_API_KEY"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_memory[-10:]
    )
    return response.choices[0].message.content

# ================= MAIN LOOP =================

def run_jarvis():
    speak("Jarvis online. Awaiting your command.")

    while True:
        text = listen()
        if not text:
            continue

        print("You:", text)

        if WAKE_WORD in text:
            speak("Yes?")
            command = listen()
            intent = get_intent(command)
            handle_action(intent, command)

# ================= START =================

if __name__ == "__main__":
    run_jarvis()


