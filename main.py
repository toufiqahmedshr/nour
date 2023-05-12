from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# initialize speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id) # 0 = male, 1 = female
activation_word = "computer"

def say(text, rate=120):
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

def parse_command():
    listener = sr.Recognizer()
    print("Listening for a command...")

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input = listener.listen(source)
    
    try:
        print("Recognizing speech...")
        query = listener.recognize_google(input, language="en_gb")
        print(f"Input: {query}")
    except Exception as ex:
        print("I did not quite catch that.")
        say("I did not quite catch that.")
        print(ex)
        return None
    
    return query

if __name__ == "__main__":
    say("All systems nominal.")

    while True:
        # parse query as list
        query = parse_command().lower().split()

        if query[0] == activation_word:
            query.pop(0)

            # list commands
            if query[0] == "tell":
                if "hello" in query:
                    say("Greetings, all.")
                else:
                    query.pop(0)
                    _query = " ".join(query)
                    say(_query)
                
