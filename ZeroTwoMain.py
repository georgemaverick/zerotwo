import openai
import speech_recognition as sr
import pyttsx3
import requests
import json
import random
import sys
import tkinter as tk
import datetime

#GUI Program:
def main():
    # Create an instance of the assistant
    assistant = MyAssistant()

    # Create a GUI window
    window = tk.Tk()
    window.title("My Assistant")

    # Add a label to the window
    label = tk.Label(window, text="Hello! How can I assist you?")
    label.pack()

    # Add an entry field to the window
    entry = tk.Entry(window)
    entry.pack()

    # Add a button to the window
    button = tk.Button(window, text="Send", command=lambda: assistant.process_input(entry.get()))
    button.pack()

    # Start the GUI loop
    window.mainloop()

#Json File
knowledge_base = {}
with open('C:\\Users\\GOD\\Desktop\\knowledge_base.json', 'r') as f:
    knowledge_base = json.load(f)
   



# Initialize OpenAI API key
openai.api_key = "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"

# Initialize Text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # change voice to female
engine.setProperty('rate', 160) # set rate to 150 words per minute
engine.setProperty('volume', 0.9) # set volume to 80%


# Greeting message
greeting = ["Hello there, how can I help you?", "Heyy.. Whats up?, what can I do?", "Hello!, How can I help you","Vaanakkam, What can I do for you?", "Hi there!, I am your personal assistant. Let me know what can I help you with."]
engine.say(random.choice(greeting))
engine.runAndWait()

#Define function to load json file content.
def load_knowledge_base():
    knowledge_base = {}
    with open('knowledge_base.json', 'r') as f:
        knowledge_base = json.load(f)
    return knowledge_base
# Define function to handle user commands
def process_command(command, knowledge_base):
        if command in knowledge_base:
            engine.say("Loading from Knowledge source....")
            return knowledge_base[command]
        
        elif 'weather' in command:
            # code for getting weather
            api_key = '96ddf6c964466adc3834ffd11fa56493'
            base_url = 'http://api.openweathermap.org/data/2.5/weather?'
            city_name = 'Chennai'
            complete_url = base_url + 'appid=' + api_key + '&q=' + city_name
            response = requests.get(complete_url)
            data = response.json()
            weather = data['weather'][0]['description']
            temp = round((data['main']['temp'] - 273.15), 1)
            response_text = f'The weather is {weather} and the temperature is {temp} degrees Celsius'
            return response_text
        
        elif 'time' in command:
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            response_text = f"The time is {time_str}"
            return response_text
        
        elif 'date' in command:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            response_text = f"Today is {today}"
            return response_text

        else:

            # Use GPT-2 to generate response
            prompt = f"I want to {command}"
            response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=180,
            n=1,
            stop=None,
            temperature=0.7
            )
            response_text = response.choices[0].text.strip()
            # Store the response from GPT-2 in the knowledge base
            knowledge_base[command] = response_text
            with open('knowledge_base.json', 'w') as f:
                json.dump(knowledge_base, f)
                return response_text

# Define function to get correct answer from the user
def get_correct_answer(question):
    engine.say(f"I'm sorry, I don't know the answer to that. Can you please tell me {question}")
    engine.runAndWait()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        correct_answer = r.recognize_google(audio)
        print(f"Correct answer: {correct_answer}")
        return correct_answer
    except sr.UnknownValueError:
        print("I'm sorry, I didn't understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Define function to handle user input
def process_input(stop_flag=False):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        if stop_flag:
            return
        if command == "Exit voice recognition":
            sys.exit()
        response_text = process_command(command, knowledge_base)  # add knowledge_base argument
        if response_text:
            engine.say(response_text)
            engine.runAndWait()
        else:
            print("I'm sorry, I didn't understand that.")
            question = command
            correct_answer = get_correct_answer(question)
            if correct_answer:
                # Add the question and correct answer to the knowledge base
                knowledge_base[question] = correct_answer
                with open('knowledge_base.json', 'w') as f:
                    json.dump(knowledge_base, f)
            else:
                print("I'm sorry, I still don't understand. Can you please rephrase your command?")
        # Listen for stop command
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
        try:
            stop_command = r.recognize_google(audio)
            print(f"You said: {stop_command}")
            if stop_command == "Stop":
                return
            else:
                process_input()
        except:
            process_input()
    except sr.UnknownValueError:
        print("I'm sorry, I didn't understand that.")
        process_input()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        process_input()

# Main loop
while True:
    process_input()