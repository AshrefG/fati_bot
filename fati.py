import pyttsx3
import speech_recognition as sr
import datetime
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import requests
import fbchat
from fbchat import Client
from getpass import getpass
import pyjokes
import instaloader
import sys
import os

engine = pyttsx3.init() #'sapi5'
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voices', voices[0].id)

#txt to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#speech to txt
def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print('listening')
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)
    try:
        print('recognizing...')
        query = r.recognize_google(audio, language='en-us')
        print(f"user said: {query}")
    except Exception as e:
        speak("say that again please..")
        return "none"
    return query    

#greetings & wake
def wish():
    hour= datetime.datetime.now().hour
    if hour >=6 and hour <= 12:
        speak('good morning')
    elif hour >=12 and hour <= 18:
        speak('good afternoon') 
    elif hour >=18 and hour <= 24:
        speak('good evening')   
    else:
        speak('good night')  

    speak('I am at your service, how can I help you ?')
  
#send mail
def sendEmail(to, content):
    server = smtplib.SMTP('smt.gmail.com', 587)
    server.ehlo()
    server.starttls
    server.login('mail','pswd')
    server.sendmail('dest', to, content)
    server.close()

def execute():
    wish()
    while True:
        query = takeCommand().lower()
        #logic building
        if "location" in query or "where are we" in query:
            speak('one second, let me check')
            try:
                ip= requests.get('https://api.ipify.org').text
                print(ip)
                url = 'https://get.geojs.io/v1/ip/geo/'+ip+'.json'
                geo_req= requests.get(url)
                geo_data= geo_req.json()
                city= geo_data['city']
                country= geo_data['country']
                speak('after some digging in sir, here is an estimation of ou current location')
                speak(f'weare in {city} specifically in {country}')
            except Exception as e:
                speak('Sorry but due to network issues am not able to find our location')    
                pass

        elif "wikipedia" in query:
            speak('searching wikipedia')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)

        elif "youtube" in query:   
            webbrowser.open("www.youtube.com")

        elif "joke" in query:   
            joke = pyjokes.get_joke()
            speak(joke)     

        elif "facebook" in query:   
            webbrowser.open("www.facebook.com") 

        elif "instagram" in query:
            speak('who are we looking for')
            #un = takeCommand().lower()
            name = str(input("Name: "))
            webbrowser.open(f'www.instgram.com/{name}')
            speak('would you like to download this accounts profile picture ?')
            condition = takeCommand().lower()
            if 'yes' in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only=True)
                speak('all done')
                speak('check your folder, sir')
            else:
                pass    

        elif "tinker" in query:   
            webbrowser.open("www.tinker.tn")   

        elif "google" in query: 
            speak('sir, what are you looking for on google ?')  
            cm = takeCommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm}")   

        elif "send message" in query:
            kit.sendwhatmsg("num","this is a test",0,2)

        elif "play music" in query:
            speak('sir, what do you want to listen to ?')  
            condition = takeCommand().lower()
            #kit.playonyt(f"{yt}")
            #speak("loading song sir")
            if "my playlist" in condition:
                webbrowser.open("https://www.youtube.com/watch?v=6I44IYGyB_4&list=PLGF0--njYf7DDztccEJ6L3poV1WnnyIyi")
            elif "specific" in condition:
                speak("what song you feel like listening to ?")
                yt = takeCommand().lower()
                kit.playonyt(f"{yt}")
                speak("loading song sir")

        elif "email" in query:
            try:
                speak("what should I say ?")
                content = takeCommand().lower()
                
                to= "gamoudi.fathia@gmail.com"
                sendEmail(to, content)
                speak ('email has been sent with success')
            except Exception as e:
                print(e)
                speak('sorry sir, I was not able to send the email') 

        elif "chat" in query:
            speak('that will be my pleasure sir')
            speak('what do you want to talk about')

        elif "no thanks" in query or "sleep" in query:  
            speak('am always at your service')
            break

        speak('anything else sir !')  


if __name__ == "__main__":
    while True  :
        permission = takeCommand()
        if "wake up" in permission or "hey wally" in permission or "wally" in permission:
            execute()
        elif "shut down" in permission:
            sys.exit()    