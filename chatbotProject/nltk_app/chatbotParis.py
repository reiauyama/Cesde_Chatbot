import nltk 
import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from nltk.chat.util import Chat, reflections
from scraper.models import Menu


def chatbot():
    print(f"ROBO: Hola, Soy ROBO el asistente chatbot, puedo ayudarte con \n {Menu.title} ")
chatbot()