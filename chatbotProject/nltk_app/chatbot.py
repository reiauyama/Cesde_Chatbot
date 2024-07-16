import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()

# Importar los archivos generados en el código anterior
intents = json.loads(open('intents.json', 'r', encoding='utf-8').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Pasar las palabras de oración a su forma raíz
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Convertimos la información a unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    print(f"Bag of words: {bag}")  # Imprimir la bolsa de palabras
    return np.array(bag)

# Predecir la categoría a la que pertenece la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    print(f"Prediction results: {res}")  # Imprimir los resultados de la predicción
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    print(f"Predicted category: {category}")  # Imprimir la categoría predicha
    return category

# Obtener una respuesta aleatoria
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = "\n".join(i['responses'])
            break
    print(f"Response: {result}")  # Imprimir la respuesta obtenida
    return result

def respuesta(message):
    tag = predict_class(message)
    res = get_response(tag, intents)
    return res

# Loop principal del chatbot
while True:
    message = input("Tú: ")
    if message.lower() == 'salir':
        break
    print(f"Bot:\n{respuesta(message)}")