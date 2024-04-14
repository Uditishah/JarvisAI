import speech_recognition as sr
import os
import webbrowser
import datetime
from config import apikey
import openai

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Uditi: {query}\n Jarvis: "
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    os.system(f"say {text}")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("recognising...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occured. Sorry, Try again."


if __name__ == '__main__':
    print('Welcome to A.I')
    say("Uditi chatbot A.I")
while True:
    print("Listening...")
    query = takeCommand()
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
             ["google", "https://www.google.com"], ]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]}...")
            webbrowser.open(site[1])

    # todo: Add a feature to play a specific song
    if "open music" in query:
        musicPath = "/Users/uditishah/Downloads/deep-in-the-ocean-116172.mp3"
        os.system(f"open {musicPath}")

    elif "the time" in query:
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        seconds = datetime.datetime.now().strftime("%S")
        say(f"The time is {hour} hours {minute} minutes and {seconds} seconds")

    elif "open facetime".lower() in query.lower():
        os.system(f"open /System/Applications/FaceTime.app")

    elif "Using artificial intelligence".lower() in query.lower():
        ai(prompt=query)

    elif "Jarvis Quit".lower() in query.lower():
        exit()

    elif "reset chat".lower() in query.lower():
        chatStr = ""

    else:
        print("Chatting...")
        chat(query)
    # say(query)
