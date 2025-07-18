import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
from playsound import playsound
import wikipedia
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import requests
import yagmail

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. Please tell me how may I help you")


def listen_for_command():
    """Listens for a command from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return "None"
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"

if __name__ == "__main__":
    wish_me()
    while True:
        command = listen_for_command()

        if 'search on youtube' in command:
            query = command.replace("search on youtube", "")
            speak(f"Searching for {query} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

        elif 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif 'search on google' in command:
            query = command.replace("search on google", "")
            speak(f"Searching for {query} on Google")
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif 'open google' in command:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif 'wikipedia' in command:
            speak('Searching Wikipedia...')
            command = command.replace("wikipedia", "")
            results = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'time' in command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'play music' in command:
            music_dir = 'music'
            songs = os.listdir(music_dir)
            if songs:
                song_to_play = os.path.join(music_dir, songs[0])
                speak(f"Playing {songs[0]}")
                playsound(song_to_play)
            else:
                speak("No music files found in the music directory.")

        elif 'shutdown' in command:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")

        elif 'restart' in command:
            speak("Restarting the system")
            os.system("shutdown /r /t 1")

        elif 'sleep' in command:
            speak("Putting the system to sleep")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'calculate' in command:
            # WARNING: Using eval can be a security risk.
            # This implementation is for a personal assistant and assumes trusted input.
            expression = command.replace("calculate", "").strip()
            
            # Replace words with operators
            replacements = {
                "plus": "+",
                "minus": "-",
                "times": "*",
                "x": "*",
                "divided by": "/",
                "power": "**",
            }
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)
            
            try:
                # A simple way to remove any other words that are not part of the expression
                allowed_chars = "0123456789+-*/.() "
                safe_expression = "".join(filter(lambda char: char in allowed_chars, expression))
                result = eval(safe_expression)
                speak(f"The result is {result}")
            except Exception as e:
                speak("Sorry, I could not perform the calculation.")
                print(f"Error during calculation: {e}")

        elif 'set volume' in command:
            try:
                level = int(command.split()[-1])
                if 0 <= level <= 100:
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevelScalar(level / 100, None)
                    speak(f"Volume set to {level} percent")
                else:
                    speak("Please specify a volume level between 0 and 100.")
            except:
                speak("Sorry, I could not adjust the volume.")

        elif 'set brightness' in command:
            try:
                level = int(command.split()[-1])
                if 0 <= level <= 100:
                    sbc.set_brightness(level)
                    speak(f"Brightness set to {level} percent")
                else:
                    speak("Please specify a brightness level between 0 and 100.")
            except:
                speak("Sorry, I could not adjust the brightness.")

        elif 'create file' in command:
            try:
                filename = command.split("create file")[-1].strip()
                with open(filename, 'w') as f:
                    f.write('')
                speak(f"File '{filename}' created successfully.")
            except:
                speak("Sorry, I could not create the file.")

        elif 'create folder' in command:
            try:
                foldername = command.split("create folder")[-1].strip()
                os.makedirs(foldername)
                speak(f"Folder '{foldername}' created successfully.")
            except:
                speak("Sorry, I could not create the folder.")

        elif 'rename file' in command:
            try:
                parts = command.replace("rename file", "").strip().split(" to ")
                old_name = parts[0]
                new_name = parts[1]
                os.rename(old_name, new_name)
                speak(f"File '{old_name}' renamed to '{new_name}'.")
            except:
                speak("Sorry, I could not rename the file.")

        elif 'delete file' in command:
            try:
                filename = command.split("delete file")[-1].strip()
                os.remove(filename)
                speak(f"File '{filename}' deleted successfully.")
            except:
                speak("Sorry, I could not delete the file.")

        elif 'search for file' in command:
            try:
                filename = command.split("search for file")[-1].strip()
                results = []
                for root, dirs, files in os.walk("C:/"):
                    if filename in files:
                        results.append(os.path.join(root, filename))
                if results:
                    speak(f"Found {len(results)} files:")
                    for result in results:
                        print(result)
                        speak(result)
                else:
                    speak(f"No file named '{filename}' found.")
            except:
                speak("Sorry, I could not search for the file.")

        elif 'what can you do' in command:
            speak("I can perform a variety of tasks, including controlling your system, managing files, searching the web, performing calculations, translating text, and even sending emails. Just give me a command!")

        elif 'define' in command:
            try:
                word = command.replace("define", "").strip()
                response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
                if response.status_code == 200:
                    definition = response.json()[0]['meanings'][0]['definitions'][0]['definition']
                    speak(f"The definition of {word} is: {definition}")
                else:
                    speak(f"Sorry, I could not find a definition for {word}.")
            except:
                speak("Sorry, I could not find a definition for the word.")

        elif 'send email' in command:
            try:
                speak("Who should I send the email to?")
                to = listen_for_command()
                if to == "None": continue
                speak("What is the subject?")
                subject = listen_for_command()
                if subject == "None": continue
                speak("What should I say in the email?")
                body = listen_for_command()
                if body == "None": continue

                # Securely get email credentials from environment variables
                email_user = os.environ.get('EMAIL_USER')
                email_password = os.environ.get('EMAIL_PASSWORD')

                if not email_user or not email_password:
                    speak("Email credentials are not configured. Please set the EMAIL_USER and EMAIL_PASSWORD environment variables.")
                    continue

                yag = yagmail.SMTP(email_user, email_password)
                yag.send(to=to, subject=subject, contents=body)
                speak("Email sent successfully.")
            except Exception as e:
                speak("Sorry, I could not send the email.")
                print(f"Error sending email: {e}")

        elif "exit" in command:
            speak("Goodbye!")
            break