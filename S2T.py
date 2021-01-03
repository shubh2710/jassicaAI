import speech_recognition as SRG
import requests
store = SRG.Recognizer()
import time





def startListening(timesec):
    time.sleep(int(timesec))
    with SRG.Microphone() as s:
        text_output=""

        print("Speak...")
        nameCall=""
        store.adjust_for_ambient_noise(s)
        audio_input = store.record(s, duration=3)
        try:
            nameCall = store.recognize_google(audio_input)
            print(nameCall)
            if nameCall.lower()== "jessica":
                print("word found")
                with SRG.Microphone() as s:
                    store.adjust_for_ambient_noise(s)
                    audio_input = store.record(s, duration=5)
                    text_output = store.recognize_google(audio_input)
                    text_output=text_output.lower()
                    if(len(text_output)>1):
                        r = requests.post('http://localhost:8080/crisper/v1/exec',json={'command':text_output})
                        print(r.text)
                print("Text converted from audio:\n")
                print(text_output)
                text_output=""
                print("Finished!!")
                print("Execution time:",time.strftime("%I:%M:%S"))
        except:
            print("Couldn't process the audio input.")

        text_output=text_output.lower()
        if(len(text_output)>1):
            r = requests.post('http://localhost:8080/crisper/v1/exec',json={'command':text_output})
            print(r.text)

while True:
    startListening(0)

    #thread=threading.Thread(target=startListening, args=(1,))
    #thread.start()