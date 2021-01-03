from Config import app

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import re
import json
import random

intents = json.loads(open('intents.json').read())
slotsValue = json.loads(open('slotsValue.json').read())
slotConditionResponse = json.loads(open('SlotConditionResponse.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=True)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            resultRegex = random.choice(i['responsesRegex'])
            slots=i['slots']
            type=i['type']
            patterns=i['patterns']
            actionType=i['actionType']
            break
    return_list = []
    return_list.append({'tag': tag, 'result': result,'resultRegex': resultRegex,'slots':slots,'type':type,'patterns':patterns,'actionType':actionType})
    return return_list


def fillSlots(msg, res):
    for i in slotsValue:
        print(i)
    allSlotsList=slotsValue

    tag=res[0]['tag']
    responce=res[0]['result']
    actionType=res[0]['actionType']
    slots=res[0]['slots']
    responseType=res[0]['type']
    filledslots={}

#find values
    for i in slots:
        for value in allSlotsList[i]['values']:
            filledslots[i] = None
            if msg.find(value)>-1:
                print("found slot: "+value)
                filledslots[i] = value
                break

    slotMissingValues=[]
    responceMissingSlots="Some values are missing like "

#check is missing
    for i in filledslots:
        if filledslots[i]==None:
            slotMissingValues.append(i)
            responceMissingSlots=responceMissingSlots+i+",";
            actionType="Err"

#fill and replace
    if(len(slotMissingValues)==0):
        for i in filledslots:
            responce=responce.replace('@'+i,filledslots[i])
    else:
        responce= responceMissingSlots
#check extra msg
    for i in slotConditionResponse:
        isfind=False
        for keys in list(slotConditionResponse[i]['when'].keys()):
            if(filledslots[keys]!=None and filledslots[keys]==slotConditionResponse[i]['when'][keys]):
                isfind=True
            else:
                isfind=False
                break
        if(isfind==True):
            responce=responce+","+slotConditionResponse[i]['extraMsg']
            break



    responceModel={}
    responceModel['intent']=tag
    responceModel['responce']=responce
    responceModel['slots']=filledslots
    responceModel['missingSlots']=slotMissingValues
    responceModel['actionType']=actionType
    responceModel['responseType']=responseType
    return responceModel

def defualtResponce(msg, res):

    tag=res[0]['tag']
    responseType=res[0]['type']
    responce=res[0]['result']
    actionType=res[0]['actionType']
    slots=res[0]['slots']

    responceModel={}
    responceModel['intent']=tag
    responceModel['responce']=responce
    responceModel['slots']={}
    responceModel['missingSlots']={}
    responceModel['actionType']=actionType
    responceModel['responseType']=responseType
    return responceModel


def fillPattern(msg, resList):
    #(.*)
    pattens=resList[0]['patterns']
    responce=resList[0]['result']
    regexResponse=resList[0]['resultRegex']
    tag=resList[0]['tag']
    actionType=resList[0]['actionType']
    responseType=resList[0]['type']
    print(pattens)
    for i in pattens:
        res=searchStar(i,msg,regexResponse)
        if(res!= None):
            responceModel={}
            responceModel['intent']=tag
            responceModel['responce']=res['textResponse']
            responceModel['pattrenValue']=res['value']
            responceModel['slots']={}
            responceModel['responseType']=responseType
            responceModel['missingSlots']={}
            responceModel['actionType']=actionType
            return responceModel

    responceModel={}
    responceModel['intent']=tag
    responceModel['responce']=responce
    responceModel['slots']={}
    responceModel['missingSlots']={}
    responceModel['actionType']=actionType
    responceModel['responseType']=responseType
    return responce

def searchStar(pattern,msg,regexResponse):
    pattern=pattern.replace('$','(.*)')
    title_search = re.search(pattern, msg, re.IGNORECASE)
    if title_search:
        response={}
        title = title_search.group(1)
        response['value']=title
        response['textResponse']=regexResponse.replace("$",title)
        return response
    return None

def chatbot_response(msg):
    print(app.config)
    model = app.config["ai_model"]
    ints = predict_class(msg, model)
    resList = getResponse(ints, intents)
    if(resList[0]['type']=='slot'):
        res=fillSlots(msg,resList)
    elif(resList[0]['type']=='pattern'):
        res=fillPattern(msg,resList)
    else:
        res=defualtResponce(msg,resList)
    return res

print(chatbot_response("turn on room1 alexa"))