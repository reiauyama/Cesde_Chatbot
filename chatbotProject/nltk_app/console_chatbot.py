import django
import os

import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from nltk_app.views import process_query
import nltk
while True:
    user_input = input("Tú: ")
    if user_input.lower() == 'salir':
        break
    response = process_query(user_input)
    print(f"Bot: {response}")