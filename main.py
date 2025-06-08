import speech_recognition as sr
import webbrowser
import pyttsx3 as py
import requests
import google.generativeai as genai

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
ttsx = py.init()

# Configure Gemini API
genai.configure(api_key="AIzaSyC21ywySFjA5z9pNTPPyqnkKbpgZotJtz4")  # Replace with your actual API key
for model in genai.list_models():
    print(model.name)
# News API key
newsapi = "4aba5bddd1d1456bbb08ae7bd50fe3aa"

# Speak function
def speak(text):
    print("Jarvis:", text)
    ttsx.say(text)
    ttsx.runAndWait()

# Gemini AI interaction
def ask_ai_gemini(prompt):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
  # Correct model path
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error using Gemini AI: {e}"

# Handle recognized command
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "show news" in c or "news" in c:
        speak("Fetching the latest headlines")
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        
        if response.status_code == 200:
            data = response.json()
            titles = [article['title'] for article in data.get('articles', [])]
            if titles:
                for title in titles[:5]:  # Read only top 5 to avoid spamming
                    speak(title)
            else:
                speak("Sorry, I couldn't find any news at the moment.")
        else:
            speak(f"Failed to fetch news: {response.status_code}")

    else:
        speak("Thinking...")
        ai_reply = ask_ai_gemini(c)
        # speak(ai_reply)
        print(ai_reply)

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
            
            if word.lower() == "jarvis":
                speak("Yes sir, I'm listening.")

                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    print("You said:", command)
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, waiting again...")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
        except Exception as e:
            print("Error:", e)
