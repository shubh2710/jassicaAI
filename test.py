import os
import random
import pygame, time
from gtts import gTTS
import pyttsx3
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

str1 = " "
list=sys.argv[1::]
text=(str1.join(list))

if len(list)>2:
    runtime=int(len(list)-2)
else:
    runtime=int(len(list))
mytext = text

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
