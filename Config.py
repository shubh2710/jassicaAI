from flask import Flask
from tensorflow.keras.models import load_model

app = Flask(__name__)

def loadmodel():
    model = load_model('chatbot_model.h5')
    return model

app.config['ai_model'] = loadmodel()
app.config['DEBUG'] = True