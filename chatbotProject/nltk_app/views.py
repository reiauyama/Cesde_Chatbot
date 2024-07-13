from django.shortcuts import render
import os
import sys
import django
from fuzzywuzzy import process
import nltk

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from scraper.models import SubMenu, SubSubMenu, Menu, sub3menu

nltk.download('punkt')
nltk.download('wordnet')

# Función para normalizar el texto
def normalize_text(text):
    tokens = nltk.word_tokenize(text.lower())
    lemmatizer = nltk.WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(token) for token in tokens])

def get_best_match(query, choices):
    normalized_query = normalize_text(query)
    normalized_choices = [normalize_text(choice) for choice in choices]
    best_match = process.extractOne(normalized_query, normalized_choices)
    return best_match

def process_query(query):
    # Obtener todos los títulos de las tablas para comparación
    menu_titles = Menu.objects.values_list('title', flat=True)
    submenu_titles = SubMenu.objects.values_list('title', flat=True)
    subsubmenu_titles = SubSubMenu.objects.values_list('title', flat=True)
    sub3menu_contents = sub3menu.objects.values_list('content', flat=True)

    all_titles = list(menu_titles) + list(submenu_titles) + list(subsubmenu_titles) + list(sub3menu_contents)

    best_match = get_best_match(query, all_titles)

    if best_match and best_match[1] > 70:  # umbral de similitud del 70%
        normalized_best_match = normalize_text(best_match[0])
        
        # Búsqueda en la tabla Menu
        menu_items = Menu.objects.filter(title__icontains=normalized_best_match)
        if menu_items.exists():
            related_info = SubMenu.objects.filter(menu=menu_items.first())
            return '\n'.join([f"{item.id}: {item.title}" for item in related_info])
        
        # Búsqueda en la tabla SubMenu
        submenu_items = SubMenu.objects.filter(title__icontains=normalized_best_match)
        if submenu_items.exists():
            related_info = SubSubMenu.objects.filter(submenu=submenu_items.first())
            return '\n'.join([f"{item.id}: {item.title}" for item in related_info])
        
        # Búsqueda en la tabla SubSubMenu
        subsubmenu_items = SubSubMenu.objects.filter(title__icontains=normalized_best_match)
        if subsubmenu_items.exists():
            related_info = sub3menu.objects.filter(subsubmenu=subsubmenu_items.first())
            return '\n'.join([f"{item.id}: {item.content}" for item in related_info])
        
        # Búsqueda en la tabla Sub3Menu
        sub3menu_items = sub3menu.objects.filter(content__icontains=normalized_best_match)
        if sub3menu_items.exists():
            return '\n'.join([f"{item.id}: {item.content}" for item in sub3menu_items])

    return 'No se encontró información relacionada.'

while True:
    user_input = input("Tú: ")
    if user_input.lower() == 'salir':
        break
    response = process_query(user_input)
    print(f"Bot:\n{response}")
