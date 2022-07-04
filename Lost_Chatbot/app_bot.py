from flask import Flask, request
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.update import Update
import json
import string
import pickle 
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model

app = Flask(__name__)

# Load json file
data_file = open('Lost_Chatbot/intents.json').read()
intents_json = json.loads(data_file)

# Load TF model
model = load_model('Lost_Chatbot/model.h5')

# Load Label Encoder
with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Load text vectorization
from_disk = pickle.load(open('vect.pkl', 'rb'))
vect = tf.keras.layers.TextVectorization.from_config(from_disk['config'])

vect.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
vect.set_weights(from_disk['weights'])

# Cleaning text function
def clean_text(text):
    """Preprocessing Function"""
    # konversi ke lowercase
    text = text.lower()
    # menghapus tanda baca
    tandabaca = tuple(string.punctuation)
    text = ''.join(ch for ch in text if ch not in tandabaca)
    return text

# Function Bot Response
def bot_response(text):
    text = clean_text(text)
    pred = model.predict([text])
    res = encoder.classes_[pred.argmax()] # Mencari index yang memiliki probabilitas tertinggi
    i = 0
    try:
        if vect(text).numpy().max() > 1: # If the input is known word(s)
            while i < len(intents_json['intents']):
                if res == intents_json['intents'][i]['tag']:
                    responses = intents_json['intents'][i]['responses']
                    break
                else:
                    i+=1
        else: # If only unknown word(s)
            responses = ['Maaf kawan, aku tidak mengerti perkataan mu ...']
    except: # If empty string or any error occured
        responses = ['GoBot tidak mengerti :( ...']

    # # For debugging only
    # dict_temp = []
    # for i in range(len(pred[0])):
    #     temp = {encoder.classes_[i]: pred[0][i]}
    #     dict_temp.append(temp)
    # print(dict_temp)
    # print(encoder.classes_[pred.argmax()])

    return print(np.random.choice(responses))

#######################################################

global TOKEN
TOKEN = '5340594763:AAGYSodTD4ooxnERR_BX3gpB1-WDEMouxnA'

print("Bot started...")

def start_command(update: Update , context: CallbackContext):
    update.message.reply_text("Halo! Selamat datang di Let's Get Lost GoBot!")

def help_command(update, context: CallbackContext):
    update.message.reply_text('Jika kamu butuh bantuan, kamu bisa meminta bantuan Admin kami.')

def reply(update, context):
    user_input = str(update.message.text)
    update.message.reply_text(bot_response(user_input))

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    # Dispatcher 
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, reply))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()   

