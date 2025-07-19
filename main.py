import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pyautogui
import time
import os
import subprocess
from playsound import playsound
import wikipedia
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import requests
import yagmail
from groq import Groq
from newsapi import NewsApiClient
from github import Github
import pyperclip
from dotenv import load_dotenv

load_dotenv()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def open_with_profile(url):
    """Opens a URL in a specific Chrome profile."""
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    profile_directory = "Profile 3"
    subprocess.Popen([chrome_path, f"--profile-directory={profile_directory}", url])


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning, Riddhiman!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, Riddhiman!")
    else:
        speak("Good Evening, Riddhiman!")
    speak("I am Jarvis. Please tell me how may I help you")


def chat_with_groq(query):
    """Sends a query to the Groq API, prints the response, and speaks it."""
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        response = chat_completion.choices[0].message.content
        print(f"Jarvis: {response}")
        speak(response)
    except Exception as e:
        print(f"Error in chat_with_groq: {e}")
        speak("Sorry, I could not connect to the chat service.")


def get_world_news():
    """Fetches and speaks the top 5 world news headlines."""
    try:
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            speak("The News API key is not configured. Please set the NEWS_API_KEY environment variable.")
            return
        newsapi = NewsApiClient(api_key=api_key)
        top_headlines = newsapi.get_top_headlines(language='en', country='us')
        speak("Here are the top 5 world news headlines:")
        for i, article in enumerate(top_headlines['articles'][:5]):
            speak(f"Number {i+1}: {article['title']}")
    except Exception as e:
        print(f"Error in get_world_news: {e}")
        speak("Sorry, I could not fetch the world news.")


def get_financial_news():
    """Fetches and speaks the top 5 financial news headlines."""
    try:
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            speak("The News API key is not configured. Please set the NEWS_API_KEY environment variable.")
            return
        newsapi = NewsApiClient(api_key=api_key)
        top_headlines = newsapi.get_top_headlines(category='business', language='en', country='us')
        speak("Here are the top 5 financial news headlines:")
        for i, article in enumerate(top_headlines['articles'][:5]):
            speak(f"Number {i+1}: {article['title']}")
    except Exception as e:
        print(f"Error in get_financial_news: {e}")
        speak("Sorry, I could not fetch the financial news.")


def summarize_github_repo():
    """Summarizes a public GitHub repository from a URL provided in the terminal."""
    speak("Please paste the GitHub repository URL in the terminal and press Enter.")
    repo_url = input("Enter the GitHub repository URL: ")

    if not repo_url or "github.com" not in repo_url:
        speak("No valid GitHub URL was provided.")
        return

    try:
        speak("Summarizing the repository. This may take a moment.")
        # Extract owner and repo name from URL
        repo_url = repo_url.strip()
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner, repo_name = parts[0], parts[1]

        github_token = os.environ.get("GITHUB_TOKEN")
        g = Github(github_token)
        repo = g.get_repo(f"{owner}/{repo_name}")

        contents = []
        queue = [repo.get_contents("")]
        while queue:
            dir_contents = queue.pop(0)
            for content_file in dir_contents:
                if content_file.type == "dir":
                    queue.append(repo.get_contents(content_file.path))
                else:
                    try:
                        # Only include common text-based files
                        if content_file.name.endswith(('.py', '.js', '.html', '.css', '.md', '.txt')):
                            contents.append(content_file.decoded_content.decode('utf-8'))
                    except Exception:
                        pass  # Ignore files that can't be decoded

        full_content = "\n".join(contents)
        
        # Summarize with Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following code from a GitHub repository. Provide a high-level overview of the project's purpose, main technologies used, and key functionalities."
                },
                {
                    "role": "user",
                    "content": full_content[:8000] # Limit to avoid exceeding token limits
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        summary = chat_completion.choices[0].message.content

        print(f"Repository Summary:\n{summary}")
        speak(summary)

    except Exception as e:
        print(f"Error summarizing GitHub repo: {e}")
        speak("Sorry, I could not summarize the repository. Please check the URL.")


def listen_for_command():
    """Listens for a command, handles errors, and returns the command as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Timeout waiting for phrase to start")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        # This error is intentionally not spoken to avoid interrupting the user.
        print("Google Speech Recognition could not understand audio")
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
            open_with_profile(f"https://www.youtube.com/results?search_query={query}")

        elif 'open youtube' in command:
            speak("Opening YouTube")
            open_with_profile("https://www.youtube.com")

        elif 'search on google' in command:
            query = command.replace("search on google", "")
            speak(f"Searching for {query} on Google")
            open_with_profile(f"https://www.google.com/search?q={query}")

        elif 'open google' in command:
            speak("Opening Google")
            open_with_profile("https://www.google.com")

        elif 'play on spotify' in command:
            query = command.replace("play on spotify", "")
            speak(f"Playing {query} on Spotify")
            open_with_profile(f"https://open.spotify.com/search/{query}")
            time.sleep(5)  # Wait for the page to load
            pyautogui.click(x=1037, y=574) # Adjust these coordinates if necessary

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

        elif 'world news' in command:
            get_world_news()

        elif 'financial news' in command:
            get_financial_news()

        elif 'summarise github' in command:
            summarize_github_repo()

        else:
            chat_with_groq(command)