# Import the required module for text
# to speech conversion
import os
import random
import pygame, time
from gtts import gTTS
import pyttsx3

import sys

import urllib.request
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


def say(mytext):

    if(connect()):
        language = 'hi'

        r1 = random.randint(1,10000000)
        r2 = random.randint(1,10000000)


        myobj = gTTS(text=mytext, lang=language, slow=False)

        randfile = "../../"+str(r2)+"randomtext"+str(r1) +".mp3"
        myobj.save(randfile)


        pygame.init()
        pygame.mixer.music.load(randfile)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(randfile)
    else:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        for voice in voices:
            print("Voice:")
            print(" - ID: %s" % voice.id)
            print(" - Name: %s" % voice.name)
            print(" - Languages: %s" % voice.languages)
            print(" - Gender: %s" % voice.gender)
            print(" - Age: %s" % voice.age)

        engine.setProperty("languages",'hi')
        engine.setProperty('rate', 150)
        # Speed percent (can go over 100)
        engine.setProperty('volume', 0.9)
        engine.setProperty('voice', voices[1].id)
        engine.say(mytext)

        engine.runAndWait()

