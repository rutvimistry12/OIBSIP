"""
Advanced Voice Assistant (Python 3.13 Compatible)
Features:
- Speech recognition
- Text to speech
- Weather lookup
- Reminders (schedule fixed)
- Web search + open sites
- Time / Date
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests
import time
import threading
import schedule    # correct library name

# -------------------------------
# INITIAL SETUP
# -------------------------------
listener = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# -------------------------------
# LISTENING (SAFE HANDLING)
# -------------------------------

def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            try:
                r.adjust_for_ambient_noise(source, duration=0.5)
            except:
                pass
            audio = r.listen(source, timeout=6, phrase_time_limit=7)

        try:
            text = r.recognize_google(audio)
            print("You:", text)
            return text.lower()

        except:
            return ""

    except Exception as e:
        print("Microphone Error:", e)
        return ""


# -------------------------------
# WEATHER FEATURE
# -------------------------------

def get_weather(city):
    api_key = "demo-key"  # replace with real API key
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()

        if "main" in res:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            return f"Weather in {city}: {desc}, {temp}°C."
        else:
            return "City not found."

    except:
        return "Unable to fetch weather right now."


# -------------------------------
# REMINDER SYSTEM (FIXED)
# -------------------------------

def reminder_task(msg):
    speak(f"Reminder: {msg}")


def set_reminder(command):
    try:
        words = command.split()
        if "minute" in command:
            amount = int(words[words.index("in") + 1])
            message = command.split("to", 1)[1].strip()
            schedule.every(amount).minutes.do(reminder_task, message)
            speak(f"Reminder set for {amount} minute(s).")

        elif "second" in command:
            amount = int(words[words.index("in") + 1])
            message = command.split("to", 1)[1].strip()
            schedule.every(amount).seconds.do(reminder_task, message)
            speak(f"Reminder set for {amount} second(s).")

        else:
            speak("I can set reminders only in minutes or seconds as of now.")

    except:
        speak("I could not understand your reminder request.")


def scheduler_thread():
    while True:
        try:
            schedule.run_pending()
        except:
            pass
        time.sleep(1)


# -------------------------------
# COMMAND HANDLER
# -------------------------------

def handle_command(cmd):
    if not cmd:
        return

    # Greet
    if any(w in cmd for w in ["hello", "hi", "hey"]):
        speak("Hello! How can I help you today?")

    # Time
    elif "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    # Date
    elif "date" in cmd or "day" in cmd:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")

    # Weather
    elif "weather" in cmd:
        speak("Please tell me the city name.")
        city = listen()
        if city:
            speak(get_weather(city))
        else:
            speak("I didn't get the city name.")

    # Reminder
    elif "remind me" in cmd:
        set_reminder(cmd)

    # Search
    elif cmd.startswith("search"):
        q = cmd.replace("search", "").strip()
        if q:
            speak(f"Searching for {q}")
            webbrowser.open(f"https://www.google.com/search?q={q}")
        else:
            speak("What should I search?")

    # Open apps/sites
    elif "open" in cmd:
        if "youtube" in cmd:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")
        elif "google" in cmd:
            speak("Opening Google")
            webbrowser.open("https://google.com")
        elif "github" in cmd:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")
        else:
            speak("Website not supported yet.")

    # Exit
    elif any(w in cmd for w in ["exit", "quit", "stop", "bye"]):
        speak("Goodbye!")
        exit()

    else:
        speak("I didn't understand that. Try asking time, weather, or search.")


# -------------------------------
# MAIN LOOP
# -------------------------------

def main():
    speak("Voice Assistant Started. How can I help?")

    # Start reminder thread
    t = threading.Thread(target=scheduler_thread, daemon=True)
    t.start()

    while True:
        command = listen()
        handle_command(command)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
