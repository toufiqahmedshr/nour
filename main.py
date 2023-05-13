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

# config webbrowser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

# wolframalpha client
app_ID = "VURTKJ-ATER3XUG5V"
wolframalpha_client = wolframalpha.Client(app_id=app_ID)

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

def wiki_search(query=""):
    results = wikipedia.search(query)
    if not results:
        print("No wikipedia results.")
        return "No wikipedia results."
    try:
        wiki_page = wikipedia.page(results[0])
    except wikipedia.DisambiguationError as err:
        wiki_page = wikipedia.page(err.options[0])
    print(wiki_page.title)
    wiki_summary = str(wiki_page.summary)
    return wiki_summary

def list_or_dict(var):
    if isinstance(var, list):
        return var[0]["plaintext"]
    else:
        return var["plaintext"]

def search_wolframalpha(query=""):
    response = wolframalpha_client.query(query)

    # @success: wolfram alpha was able to resolve the query
    # @numpods: number of results returned
    # pod: list of results, can also contain subpods
    if response["@success"] == "false":
        return "Could not compute."
    # query resolved
    else:
        result = ""
        # question
        pod0 = response["pod"][0]
        pod1 = response["pod"][1]
        # may contain the answer, has highest confidence value
        # if it's primary, or has title or result, or definition, then it's official result
        if (("result") in pod1["@title"].lower()) or (pod1.get("@primary", "false") == "true") or ("definition" in pod1["@title"].lower()):
            # get the result
            result = list_or_dict(pod1["subpod"])
            # remove bracketed section
            return result.split("(")[0]
        else:
            question = list_or_dict(pod0["subpod"])
            # remove bracketed section
            return question.split("(")[0]
            # search wikipedia instead
            # say("Computation failed. Querying universal databank.")
            # return wiki_search(question)



# main loop
if __name__ == "__main__":
    say("All systems nominal.")
    exit_flag = False
    while not exit_flag:
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
            
            # web navigation
            if query[0] == "go" and query[1] == "to":
                say("Opening...")
                query = " ".join(query[2:])
                webbrowser.get("chrome").open_new(query)

            # query in wikipedia
            if query[0] == "wikipedia":
                query = " ".join(query[1:])
                say("Querying the universal databank...")
                results = wiki_search(query)
                say(results)
            
            # wolframalpha
            if query[0] == "compute":
                query = " ".join(query[1:])
                say("Computing...")
                try:
                    result = search_wolframalpha(query)
                    say(result)
                except:
                    say("Unable to compute.")

            # take notes
            if query[0] == "log" or query[0] == "note":
                say("Ready to record you note...")
                note = parse_command().lower()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                timestamp_ = timestamp.replace(" ", "_")
                timestamp_ = timestamp_.replace(":", "-")
                with open("notes/note_%s.txt" % timestamp_, "w") as new_file:
                    new_file.write("Timestamp: %s\n\n" % timestamp)
                    new_file.write(note)
                say("Note logged.")

            if query[0] == "exit" or query[0] == "terminate":
                say("I hope you found me helpful. Goodbye, until next time.")
                exit_flag = True
            
            query = "" # empty the query list
